from contextvars import ContextVar
from typing import Optional

from django.db import models
from django.utils import timezone
from django_tg_bot_framework.models import (
    BaseStateMachineDump,
    TgUserProfileMixin,
)

# Will be initialized with current conversation object by state machine runner before states methods run.
conversation_var: ContextVar['Conversation'] = ContextVar('conversation_var')
language_code: ContextVar[Optional[str]] = ContextVar('language_code', default=None)


class Conversation(BaseStateMachineDump, TgUserProfileMixin):
    tg_chat_id = models.CharField(
        'Id чата в Tg',
        max_length=50,
        unique=True,
        db_index=True,
        help_text='Id чата в Tg, где пользователь общается с ботом.',
    )
    started_at = models.DateTimeField(
        "когда начат",
        db_index=True,
        default=timezone.now,
        help_text="Диалог начинается, когда пользователь присылает боту своё первое сообщение в Tg.",
    )

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
        constraints = [
            *BaseStateMachineDump._meta.constraints,
            *TgUserProfileMixin._meta.constraints,
        ]
