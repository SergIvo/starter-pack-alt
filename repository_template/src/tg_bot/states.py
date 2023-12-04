from textwrap import dedent

from tg_api import (
    SendMessageRequest,
    EditMessageReplyMarkupRequest,
    EditMessageTextRequest,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from yostate import Router, Locator

from django_tg_bot_framework import (
    PrivateChatStateMachine,
    PrivateChatState,
    PrivateChatMessageReceived,
    PrivateChatCallbackQuery,
)
from django_tg_bot_framework.funnels import AbstractFunnelEvent

from trigger_mailing import funnels as trigger_funnels
from trigger_mailing.state_machine import (
    state_machine as trigger_funnel_state_machine,
    FIRST_MAILING_FUNNEL_SLUG,
    SECOND_MAILING_FUNNEL_SLUG,
)

from .models import Conversation
from .decorators import redirect_menu_commands, announce_locator

router = Router(decorators=[redirect_menu_commands, announce_locator])

state_machine = PrivateChatStateMachine(
    router=router,
    session_model=Conversation,
    context_funcs=[
        trigger_funnel_state_machine.process_collected,
        lambda: AbstractFunnelEvent.set_default_tg_user_id(
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
                            text='Go back to welcome message',
                            callback_data='welcome',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='Trigger second mailing',
                            callback_data='trigger_second_mailing',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='Go to extra buttons',
                            callback_data='extra_buttons',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='Language list',
                            callback_data='language_list',
                        ),
                    ],
                ],
            ),
        ).send()

        trigger_funnel_state_machine.push_event(trigger_funnels.LeadNavigatedToMainMenu())

        SendMessageRequest(
            text='First mailing was triggered. Wait for a minute...',
            chat_id=Conversation.current.tg_chat_id,
        ).send()

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        match callback_query.data:
            case 'welcome':
                return Locator('/welcome/')
            case 'trigger_second_mailing':
                trigger_funnel_state_machine.push_event(
                    trigger_funnels.LeadLaunchedSecondMailing(),
                )
                SendMessageRequest(
                    text='Second mailing was triggered. Wait for a minute...',
                    chat_id=Conversation.current.tg_chat_id,
                ).send()
            case 'extra_buttons':
                return Locator('/extra-buttons/')
            case 'language_list':
                return Locator('/language-list/')

    def process_message_received(self, message: PrivateChatMessageReceived) -> Locator | None:
        SendMessageRequest(
            text=f'Эхо: {message.text}',
            chat_id=Conversation.current.tg_chat_id,
        ).send()
        return Locator('/main-menu/')


@router.register('/extra-buttons/')
class MainMenuState(PrivateChatState):
    def enter_state(self) -> Locator | None:
        SendMessageRequest(
            text='There are more buttons',
            chat_id=Conversation.current.tg_chat_id,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='Back to main menu',
                            callback_data='main_menu',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='Show more buttons',
                            callback_data='show_buttons',
                        ),
                    ],
                ],
            ),
        ).send()

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        message_id = callback_query.message.message_id
        match callback_query.data:
            case 'main_menu':
                return Locator('/main-menu/')
            case 'show_buttons':
                EditMessageReplyMarkupRequest(
                    message_id=message_id,
                    chat_id=Conversation.current.tg_chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text='Back to main menu',
                                    callback_data='main_menu',
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text='Hide buttons',
                                    callback_data='hide_buttons',
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text='Do nothing',
                                    callback_data='nothing',
                                ),
                                InlineKeyboardButton(
                                    text='Language list',
                                    callback_data='language_list',
                                ),
                            ],
                        ],
                    ),
                ).send()
            case 'hide_buttons':
                EditMessageReplyMarkupRequest(
                    message_id=message_id,
                    chat_id=Conversation.current.tg_chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text='Back to main menu',
                                    callback_data='main_menu',
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text='Show more buttons',
                                    callback_data='show_buttons',
                                ),
                            ],
                        ],
                    ),
                ).send()
            case 'nothing':
                SendMessageRequest(
                    text='This button does nothing',
                    chat_id=Conversation.current.tg_chat_id,
                ).send()
            case 'language_list':
                return Locator('/language-list/')


LANGUAGES = ['Python', 'Ruby', 'TypeScript', 'Golang', 'Lua', 'Rust', 'C#', 'Java']


@router.register('/language-list/')
class MainMenuState(PrivateChatState):
    def enter_state(self) -> Locator | None:
        SendMessageRequest(
            text=f'Selected language: {LANGUAGES[0]}',
            chat_id=Conversation.current.tg_chat_id,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='->',
                            callback_data='next',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='Back to main menu',
                            callback_data='main_menu',
                        ),
                    ],
                ],
            ),
        ).send()

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        message_id = callback_query.message.message_id
        current_language = callback_query.message.text.lstrip('Selected language: ')
        current_lang_index = LANGUAGES.index(current_language)

        navigation_keys = [
                 InlineKeyboardButton(
                     text='<-',
                     callback_data='previous',
            ),
                 InlineKeyboardButton(
                     text='->',
                     callback_data='next',
            ),
        ]
        
        new_keyboard=[
            navigation_keys,
            [
                InlineKeyboardButton(
                    text='Back to main menu',
                    callback_data='main_menu',
                )
            ],
        ]

        match callback_query.data:
            case 'main_menu':
                return Locator('/main-menu/')
            case 'previous':
                previous_index = current_lang_index - 1 
                if previous_index == 0:
                    navigation_keys.pop(0)
                EditMessageTextRequest(
                    message_id=message_id,
                    text=f'Selected language: {LANGUAGES[previous_index]}',
                    chat_id=Conversation.current.tg_chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=new_keyboard
                    )
                ).send()
            case 'next':
                next_index = current_lang_index + 1
                if next_index == len(LANGUAGES) - 1:
                    navigation_keys.pop(1)
                EditMessageTextRequest(
                    message_id=message_id,
                    text=f'Selected language: {LANGUAGES[next_index]}',
                    chat_id=Conversation.current.tg_chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=new_keyboard
                    )
                ).send()


@router.register('/first-trigger-mailing/')
class FirstTriggerMailingState(PrivateChatState):

    def enter_state(self) -> Locator | None:
        mailing_text = dedent('''\
            *📨 1️⃣ It's a first mailing message!*

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

        trigger_funnel_state_machine.push_event(trigger_funnels.MailingWasSentToLead(
            funnel_slug=FIRST_MAILING_FUNNEL_SLUG,
        ))

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        SendMessageRequest(
            text=f'Your choice is: {callback_query.data}',
            chat_id=Conversation.current.tg_chat_id,
        ).send()

        match callback_query.data:
            case 'buy_first' | 'buy_second':
                trigger_funnel_state_machine.push_event(
                    trigger_funnels.MailingTargetActionAcceptedByLead(
                        action=callback_query.data,
                        funnel_slug=FIRST_MAILING_FUNNEL_SLUG,
                    ),
                )
            case 'stop_mailing':
                trigger_funnel_state_machine.push_event(trigger_funnels.LeadUnsubscribed(
                    funnel_slug=FIRST_MAILING_FUNNEL_SLUG,
                ))


@router.register('/second-trigger-mailing/')
class SecondTriggerMailingState(PrivateChatState):
    def enter_state(self) -> Locator | None:
        mailing_text = dedent('''\
            *📨 2️⃣ It's a second mailing message!*

            Enter /start to return to Main Menu.
        ''')

        SendMessageRequest(
            text=mailing_text,
            chat_id=Conversation.current.tg_chat_id,
        ).send()

        trigger_funnel_state_machine.push_event(trigger_funnels.MailingWasSentToLead(
            funnel_slug=SECOND_MAILING_FUNNEL_SLUG,
        ))
