from functools import partial

from django.conf import settings
from django.urls import path
from django_tg_bot_framework.views import process_webhook_call

from tg_bot.models import conversation_var
from tg_bot.state_machine_runners import process_tg_update
from tg_bot.states import router

app_name = 'tg_bot'

urlpatterns = [
    path(
        '',
        process_webhook_call,
        kwargs={
            'webhook_token': settings.ENV.TG.WEBHOOK_TOKEN,
            'process_update': partial(process_tg_update, router=router, conversation_var=conversation_var),
        },
        name='process_webhook_call',
    ),
]
