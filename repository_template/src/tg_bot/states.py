from textwrap import dedent

from tg_api import SendMessageRequest, InlineKeyboardMarkup, InlineKeyboardButton
from yostate import Router, Locator

from django_tg_bot_framework import (
    PrivateChatStateMachine,
    PrivateChatState,
    PrivateChatMessageReceived,
    PrivateChatCallbackQuery,
)

from trigger_funnel import events as trigger_funnel_events
from trigger_funnel.states import state_machine as trigger_funnel_state_machine

from .models import Conversation
from .decorators import redirect_menu_commands

router = Router(decorators=[redirect_menu_commands])

state_machine = PrivateChatStateMachine(
    router=router,
    session_model=Conversation,
    context_funcs=[
        trigger_funnel_state_machine.process_collected,
        lambda: trigger_funnel_events.AbstractTriggerFunnelEvent.set_default_tg_user_id(
            Conversation.current.tg_user_id,
        ),
        *PrivateChatStateMachine.DEFAULT_CONTEXT_FUNCS,
    ],
)


@router.register('/')
class FirstUserMessageState(PrivateChatState):
    """Состояние используется для обработки самого первого сообщения пользователя боту.

    Текст стартового сообщения от пользователя игнорируется, а бот переключается в
    следующий стейт, где уже отправит пользователю приветственное сообщение.

    Если вы хотите перекинуть бота в начало диалога -- на "стартовый экран" -- , то используйте другое
    состояние с приветственным сообщением. Это нужно только для обработки первого сообщения от пользователя.
    """

    def process_message_received(self, message: PrivateChatMessageReceived) -> Locator | None:
        # Ignore any user input, redirect to welcome message
        return Locator('/welcome/')


@router.register('/welcome/')
class WelcomeState(PrivateChatState):
    def enter_state(self) -> Locator | None:
        SendMessageRequest(
            text='Welcome!',
            chat_id=Conversation.current.tg_chat_id,
        ).send()

    def process_message_received(self, message: PrivateChatMessageReceived) -> Locator | None:
        SendMessageRequest(
            text=f'Эхо: {message.text}',
            chat_id=Conversation.current.tg_chat_id,
        ).send()
        return Locator('/welcome/')


@router.register('/main-menu/')
class MainMenuState(PrivateChatState):
    def enter_state(self) -> Locator | None:
        SendMessageRequest(
            text='Main Menu',
            chat_id=Conversation.current.tg_chat_id,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='Welcome message',
                            callback_data='welcome',
                        ),
                    ],
                ],
            ),
        ).send()

        trigger_funnel_state_machine.push_event(trigger_funnel_events.LeadNavigatedToMainMenu())

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        match callback_query.data:
            case 'welcome':
                return Locator('/welcome/')

    def process_message_received(self, message: PrivateChatMessageReceived) -> Locator | None:
        SendMessageRequest(
            text=f'Эхо: {message.text}',
            chat_id=Conversation.current.tg_chat_id,
        ).send()
        return Locator('/main-menu/')


@router.register('/mailing/')
class MailingState(PrivateChatState):
    def enter_state(self) -> Locator | None:
        mailing_text = dedent('''\
            *It's a mailing message!*

            Select an appropriate option:
        ''')

        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Buy option 1',
                        callback_data='buy_first',
                    ),
                    InlineKeyboardButton(
                        text='Buy option 2',
                        callback_data='buy_second',
                    ),
                    InlineKeyboardButton(
                        text='Stop mailing me',
                        callback_data='stop_mailing',
                    ),
                ],
            ],
        )
        SendMessageRequest(
            text=mailing_text,
            chat_id=Conversation.current.tg_chat_id,
            reply_markup=reply_markup,
        ).send()

        trigger_funnel_state_machine.push_event(trigger_funnel_events.MailingWasSentToLead())

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        SendMessageRequest(
            text=f'Your choice is: {callback_query.data}',
            chat_id=Conversation.current.tg_chat_id,
        ).send()

        match callback_query.data:
            case 'buy_first' | 'buy_second':
                trigger_funnel_state_machine.push_event(
                    trigger_funnel_events.LeadAcceptedMailingCallToAction(
                        action=callback_query.data,
                    ),
                )
            case 'stop_mailing':
                trigger_funnel_state_machine.push_event(trigger_funnel_events.LeadUnsubscribed())
