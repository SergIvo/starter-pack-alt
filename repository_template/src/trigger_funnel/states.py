from datetime import timedelta
from time import time
from typing import Any

from pydantic import Field
from yostate import BaseState, Locator, Router

from . import events
from .state_machine import TriggerFunnelStateMachine


router = Router()
state_machine = TriggerFunnelStateMachine(router=router)


@router.register('/')
class StartState(BaseState):
    def process(self, event: Any) -> Locator | None:
        if isinstance(event, events.LeadNavigatedToMainMenu):
            return Locator('/mailing-queue/')


@router.register('/mailing-queue/')
class MailingQueue(BaseState):
    added_to_queue_at: float = Field(
        default_factory=time,
        description='Timestamp value lead was added to mailing queue.',
    )
    waiting_till: float = Field(
        default_factory=lambda: time() + timedelta(minutes=1).total_seconds(),
        description='Timestamp value determine a moment mailing should be send after.',
    )
    expired_after: float = Field(
        default_factory=lambda: time() + timedelta(hours=24).total_seconds(),
        description='Timestamp value determine a moment mailing is considered expired after.',
    )

    def process(self, event: Any) -> Locator | None:
        if isinstance(event, events.MailingWasSentToLead):
            return Locator('/message-sent/')


@router.register('/message-sent/')
class MessageSent(BaseState):
    message_sent_at: float = Field(default_factory=time)

    def process(self, event: Any) -> Locator | None:
        match event:
            case events.LeadAcceptedMailingCallToAction():
                return Locator('/button-pressed/', params={
                    'action_selected': event.action,
                })
            case events.LeadUnsubscribed():
                return Locator('/unsubscribed/')


@router.register('/button-pressed/')
class ButtonPressed(BaseState):
    button_pressed_at: float = Field(default_factory=time)
    action_selected: str = ''


@router.register('/unsubscribed/')
class Unsubscribed(BaseState):
    button_pressed_at: float = Field(default_factory=time)
    action_selected: str = ''
