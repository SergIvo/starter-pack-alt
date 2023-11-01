from abc import ABC
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import ClassVar

from pydantic import BaseModel, Field


class AbstractTriggerFunnelEvent(BaseModel, ABC):
    """Base abstract class to define event types supported by state machine of trigger funnel.

    Should not be instantiated. Use child classes instead to create event instances.
    """

    tg_user_id: int = Field(
        default_factory=lambda: AbstractTriggerFunnelEvent._default_tg_user_id.get(),
        description='Use `set_default_tg_user_id` class method as an context manager to setup default value. ',
    )

    _default_tg_user_id: ClassVar[ContextVar[int]] = ContextVar(
        '_default_tg_user_id',
    )

    class Config:
        validate_all = True
        extra = 'forbid'
        allow_mutation = True

    @classmethod
    @contextmanager
    def set_default_tg_user_id(cls, tg_user_id: int):
        """Set default value to tg_user_id attribute for all instances of child classes."""
        var_token: Token = cls._default_tg_user_id.set(tg_user_id)
        try:
            yield
        finally:
            cls._default_tg_user_id.reset(var_token)


class LeadNavigatedToMainMenu(AbstractTriggerFunnelEvent):
    pass


class MailingWasSentToLead(AbstractTriggerFunnelEvent):
    pass


class LeadAcceptedMailingCallToAction(AbstractTriggerFunnelEvent):
    action: str = Field(
        default='',
        description='Action choices was selected by lead.',
    )


class LeadUnsubscribed(AbstractTriggerFunnelEvent):
    pass
