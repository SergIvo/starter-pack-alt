import logging
from textwrap import dedent
from time import sleep

from django.core.management.base import BaseCommand
from django.db import transaction

from yostate import Locator

from tg_bot.states import state_machine as primary_state_machine

from ...models import Lead

logger = logging.getLogger('trigger_funnel.mailing')


def track_and_run_mailing(  # noqa CCR001
    *,
    reindex_timeout: int,
) -> None:
    logger.info('Tracking for new mailing tasks started.')

    while True:
        lead: Lead | None = None
        try:
            with transaction.atomic(durable=True):
                lead = (
                    Lead.objects
                    .select_for_update()  # lock record till processing end
                    .annotate_with_tg_chat_id()
                    .exclude(tg_chat_id=None)
                    .exclude_mailing_failed()
                    .ready_for_mailing()
                    .order_by('state_machine_locator__params__added_to_queue_at')
                    .first()
                )

                if not lead:
                    logger.debug('Sleeping for %s seconds.', reindex_timeout)
                    sleep(reindex_timeout)
                    continue

                logger.info('New mailing task are found. Lead tg_user_id=%s.', lead.tg_user_id)

                with primary_state_machine.restore_session(tg_chat_id=lead.tg_chat_id) as session:
                    session.switch_to(Locator('/mailing/'))

                # protect against endless looping with a single lead
                if lead.state_machine_locator['state_class_locator'] == '/mailing-queue/':
                    lead.mailing_failure_reason = 'endless_loop'
                    lead.mailing_failure_debug_details = dedent('''\
                        Mailing should trigger lead to move to a new funnel stage but state_class_locator value\
                        remains the same.
                    ''')
                    lead.save(update_fields=['mailing_failure_reason', 'mailing_failure_debug_details'])
        except Exception as exc:
            if lead:
                lead.mailing_failure_reason = 'unhandled_exception'
                lead.mailing_failure_debug_details = repr(exc)
                lead.save(update_fields=['mailing_failure_reason', 'mailing_failure_debug_details'])
            else:
                # protect against continuous db requests for a same broken code in endless loop
                sleep(1)


class Command(BaseCommand):
    help = 'Run trigger mailing by funnel leads queue.'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument(
            '--reindex_timeout',
            type=int,
            default=5,
            help='How ofter database state will be checked for new tasks.',
        )

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])

        if verbosity > 1:
            logger.setLevel(logging.DEBUG)

        try:
            track_and_run_mailing(
                reindex_timeout=options['reindex_timeout'],
            )
        except KeyboardInterrupt:
            logger.info('Stopped by KeyboardInterrupt')
