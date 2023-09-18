from django_tg_bot_framework import BaseState, Router, InteractiveState
from tg_api import (
    Message,
)

from .decorators import redirect_menu_commands

router = Router(decorators=[redirect_menu_commands])


@router.register('/')
class FirstUserMessageState(InteractiveState):
    """Состояние используется для обработки самого первого сообщения пользователя боту.

    Текст стартового сообщения от пользователя игнорируется, а бот переключается в
    следующий стейт, где уже отправит пользователю приветственное сообщение.

    Если вы хотите перекинуть бота в начало диалога -- на "стартовый экран" -- , то используйте другое
    состояние с приветственным сообщением. Это нужно только для обработки первого сообщения от пользователя.
    """

    def react_on_message(self, message: Message) -> BaseState | None:
        # Ignore any user input, redirect to welcome message
        return router.locate('/welcome/')


@router.register('/welcome/')
class WelcomeState(InteractiveState):
    def enter_state(self) -> BaseState | None:
        # TODO send welcome message to user with buttons
        pass

    def react_on_message(self, message: Message) -> BaseState | None:
        # TODO send message on response to user text input, redirect to new state
        pass

    def react_on_inline_keyboard(self, message: Message, pressed_button_payload: str) -> BaseState | None:
        # TODO send message on response to user button, redirect to new state
        pass

# TODO add one more state class to demostrate redirect from WelcomeState
# TODO add some parameters to new state class to demostrate state parametrization
