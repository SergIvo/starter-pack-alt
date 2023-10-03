from typing import Type, Any
from django_tg_bot_framework import BaseState, Router


def select_new_state_if_menu_command(router: Router, text: str) -> BaseState | None:
    input_to_locator_mapping = {
        '/start': '/main-menu/',
    }
    match text.split():
        case _ if input_to_locator_mapping.get(text):
            return router.locate(input_to_locator_mapping[text])
        case _:
            return None


def redirect_menu_commands(state_class: Type[BaseState]) -> Type[BaseState]:
    class WrappedStateClass(state_class):
        def process(self, event: Any) -> BaseState:
            message = event.message or event.callback_query.message
            new_state = select_new_state_if_menu_command(self.router, message.text)
            if new_state:
                return new_state
            return super().process(event=event)
    return WrappedStateClass
