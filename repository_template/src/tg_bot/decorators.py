from typing import Type, Any
from yostate import Locator
from tg_api import SendMessageRequest

from django_tg_bot_framework import (
    PrivateChatState,
    PrivateChatMessageReceived,
)

from .models import Conversation

def redirect_menu_commands(state_class: Type[PrivateChatState]) -> Type[PrivateChatState]:
    class WrappedStateClass(state_class):
        def process(self, event: Any) -> Locator:
            if isinstance(event, PrivateChatMessageReceived):
                text = event.text or ''

                match text.split():
                    case ['/start']:
                        return Locator('/main-menu/')
                    case ['/welcome']:
                        return Locator('/welcome/')

            return super().process(event=event)
    return WrappedStateClass


def announce_locator(state_class: Type[PrivateChatState]) -> Type[PrivateChatState]:
    class WrappedStateClass(state_class):
        def enter_state(self) -> Locator | None:
            locator = self.locator.state_class_locator
            SendMessageRequest(
                text=f'Новый локатор: {locator}',
                chat_id=Conversation.current.tg_chat_id
            ).send()
            return super().enter_state()
    return WrappedStateClass
