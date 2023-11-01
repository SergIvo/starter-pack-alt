from collections import ChainMap
from contextlib import contextmanager
from contextvars import ContextVar, Token
import logging
from typing import final

from django.db import transaction

from pydantic import validate_arguments, ValidationError
from yostate import Router, Crawler, Locator, LocatorError

from . import events
from .models import Lead

logger = logging.getLogger('trigger_funnel')


@final
class TriggerFunnelStateMachine:
    router: Router
    _unprocessed_events_queue: ContextVar[list[events.AbstractTriggerFunnelEvent]] = ContextVar(
        '_unprocessed_events_queue',
    )

    @validate_arguments
    def __init__(
        self,
        *,
        router: Router,
    ):
        self.router = router

    def _create_crawler(self, *, lead: Lead) -> Crawler:
        crawler = Crawler(router=self.router)

        if lead.state_machine_locator:
            try:
                restored_locator = Locator.parse_obj(lead.state_machine_locator)
                crawler.restore(restored_locator)
            except ValidationError:
                logger.warning(
                    'Reset invalid state locator of funnel lead tg_user_id=%s',
                    lead.tg_user_id,
                )
            except LocatorError:
                logger.warning(
                    'Reset not found state locator of funnel lead tg_user_id=%s',
                    lead.tg_user_id,
                )

        if not crawler.attached:
            crawler.switch_to(Locator('/'))

        return crawler

    @validate_arguments
    def process_many(self, events: list[events.AbstractTriggerFunnelEvent]) -> None:
        """Restore leads from db, process funnel events and save leads to db."""
        tg_user_ids = {event.tg_user_id for event in events}

        with transaction.atomic():
            leads_affected = (
                Lead.objects
                .select_for_update()  # lock record till processing end
                .filter(tg_user_id__in=tg_user_ids)
            )
            old_leads_mapping = {lead.tg_user_id: lead for lead in leads_affected}
            new_leads_mapping: dict[int, Lead] = {}
            leads_mapping = ChainMap(
                old_leads_mapping,
                new_leads_mapping,
            )
            for event in events:
                lead = leads_mapping.get(event.tg_user_id)

                if not lead:
                    lead = Lead(tg_user_id=event.tg_user_id)
                    new_leads_mapping[lead.tg_user_id] = lead

                crawler = self._create_crawler(lead=lead)
                crawler.process(event)

                lead.state_machine_locator = crawler.current_state.locator.dict(by_alias=True)

            if old_leads_mapping:
                Lead.objects.bulk_update(old_leads_mapping.values(), fields=['state_machine_locator'])

            if new_leads_mapping:
                Lead.objects.bulk_create(new_leads_mapping.values())

    @contextmanager
    def process_collected(self):
        """Initialize contextvar to collect funnel events, process them and update db on context exit."""
        var_token: Token = self._unprocessed_events_queue.set([])
        try:
            events_to_proccess = self._unprocessed_events_queue.get()
            yield events_to_proccess
        finally:
            self._unprocessed_events_queue.reset(var_token)

        if events_to_proccess:
            self.process_many(events_to_proccess)

    @validate_arguments
    def push_event(self, event: events.AbstractTriggerFunnelEvent) -> None:
        """Push event to unprocessed events queue.

        Should be used only inside `process_collected` context manager call.
        """
        self._unprocessed_events_queue.get().append(event)

    @validate_arguments
    def push_events(self, events: list[events.AbstractTriggerFunnelEvent]) -> None:
        """Push events to unprocessed events queue.

        Should be used only inside `process_collected` context manager call.
        """
        self._unprocessed_events_queue.get().extend(events)
