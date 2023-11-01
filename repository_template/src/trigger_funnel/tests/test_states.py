from yostate import Crawler, Locator

from ..states import router
from .. import events


def test_funnel_start_to_end_traversing():
    crawler = Crawler(router=router)
    tg_user_id = 1

    crawler.switch_to(Locator('/'))
    assert crawler.attached

    crawler.process(events.LeadNavigatedToMainMenu(tg_user_id=tg_user_id))
    current_locator = crawler.current_state.locator
    assert current_locator.state_class_locator == '/mailing-queue/'
    assert current_locator.params.get('added_to_queue_at')

    crawler.process(events.MailingWasSentToLead(tg_user_id=tg_user_id))
    current_locator = crawler.current_state.locator
    assert current_locator.state_class_locator == '/message-sent/'
    assert current_locator.params.get('message_sent_at')

    crawler.process(events.LeadAcceptedMailingCallToAction(tg_user_id=tg_user_id))
    current_locator = crawler.current_state.locator
    assert current_locator.state_class_locator == '/button-pressed/'
    assert current_locator.params.get('button_pressed_at')
