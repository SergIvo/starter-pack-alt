from functools import partial

import pytest

from ..states import state_machine
from .. import events
from ..models import Lead


@pytest.mark.django_db
def test_funnel_start_to_end_traversing():
    tg_user_id = 1

    events_queue = [
        events.LeadNavigatedToMainMenu(tg_user_id=tg_user_id),
        events.MailingWasSentToLead(tg_user_id=tg_user_id),
        events.LeadAcceptedMailingCallToAction(tg_user_id=tg_user_id),
    ]

    state_machine.process_many(events_queue)

    lead = Lead.objects.get(tg_user_id=tg_user_id)
    assert lead.state_machine_locator
    assert lead.state_machine_locator['state_class_locator'] == '/button-pressed/'


@pytest.mark.django_db
def test_state_machine_saving():
    tg_user_id = 1
    get_lead = partial(Lead.objects.get, tg_user_id=tg_user_id)

    state_machine.process_many([events.LeadNavigatedToMainMenu(tg_user_id=tg_user_id)])
    assert get_lead().state_machine_locator['state_class_locator'] == '/mailing-queue/'

    state_machine.process_many([events.MailingWasSentToLead(tg_user_id=tg_user_id)])
    assert get_lead().state_machine_locator['state_class_locator'] == '/message-sent/'

    state_machine.process_many([events.LeadAcceptedMailingCallToAction(tg_user_id=tg_user_id)])
    assert get_lead().state_machine_locator['state_class_locator'] == '/button-pressed/'


@pytest.mark.django_db
def test_reaction_on_broken_state_machine_locator():
    first_lead = Lead.objects.create(tg_user_id=1, state_machine_locator={
        'state_class_locator': '/not/exist/',
    })
    second_lead = Lead.objects.create(tg_user_id=2, state_machine_locator={
        'garbage': True,
    })
    state_machine.process_many([
        events.LeadNavigatedToMainMenu(tg_user_id=first_lead.tg_user_id),
        events.LeadNavigatedToMainMenu(tg_user_id=second_lead.tg_user_id),
    ])

    updated_leads = Lead.objects.all()
    updated_state_class_locators = [lead.state_machine_locator['state_class_locator'] for lead in updated_leads]
    assert updated_state_class_locators == [
        '/mailing-queue/',
        '/mailing-queue/',
    ]


@pytest.mark.django_db
def test_events_collecting_with_direct_access():
    tg_user_id = 1

    with state_machine.process_collected() as events_queue:
        events_queue.append(events.LeadNavigatedToMainMenu(tg_user_id=tg_user_id))

        events_queue.extend([
            events.MailingWasSentToLead(tg_user_id=tg_user_id),
            events.LeadAcceptedMailingCallToAction(tg_user_id=tg_user_id),
        ])

    lead = Lead.objects.get(tg_user_id=tg_user_id)
    assert lead.state_machine_locator
    assert lead.state_machine_locator['state_class_locator'] == '/button-pressed/'


@pytest.mark.django_db
def test_events_collecting_with_contextvar():
    tg_user_id = 1

    with state_machine.process_collected():
        state_machine.push_event(events.LeadNavigatedToMainMenu(tg_user_id=tg_user_id))
        state_machine.push_events([
            events.MailingWasSentToLead(tg_user_id=tg_user_id),
            events.LeadAcceptedMailingCallToAction(tg_user_id=tg_user_id),
        ])

    lead = Lead.objects.get(tg_user_id=tg_user_id)
    assert lead.state_machine_locator
    assert lead.state_machine_locator['state_class_locator'] == '/button-pressed/'


# TODO Добавить автотест для события LeadUnsubscribed
# TODO Добавить автотест для события LeadAcceptedMailingCallToAction с полем action
