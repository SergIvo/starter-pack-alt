import pytest
from yostate import Locator, Router

from django_tg_bot_framework import PrivateChatStateMachine, PrivateChatState

# FIXME should replace with separate model independent from Starter Pack code
from tg_bot.models import Conversation as SessionModel

from ..states import state_machine as funnel_state_machine
from .. import events
from ..models import Lead


@pytest.mark.django_db
def test_integrations_with_private_chat_state_machine():
    tg_chat_id, tg_user_id = 90001, 4114

    SessionModel.objects.create(
        tg_chat_id=tg_chat_id,
        tg_user_id=tg_user_id,
    )

    router = Router()
    state_machine = PrivateChatStateMachine(
        router=router,
        session_model=SessionModel,
        context_funcs=[
            funnel_state_machine.process_collected,
            lambda: events.AbstractTriggerFunnelEvent.set_default_tg_user_id(SessionModel.current.tg_user_id),
        ],
    )

    @router.register('/main-menu/')
    class MainMenuState(PrivateChatState):
        def enter_state(self) -> Locator | None:
            funnel_state_machine.push_event(events.LeadNavigatedToMainMenu())

    with state_machine.restore_session(tg_chat_id=tg_chat_id) as session:
        session.switch_to(Locator('/main-menu/'))

    lead_locator = Lead.objects.get(tg_user_id=tg_user_id).state_machine_locator
    assert lead_locator
    assert lead_locator['state_class_locator'] == '/mailing-queue/'
