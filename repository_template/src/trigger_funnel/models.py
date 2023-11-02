from django.db import models

from time import time


class LeadQuerySet(models.QuerySet):
    def mailing_failed(self):
        return self.exclude(mailing_failure_reason='')

    def exclude_mailing_failed(self):
        return self.filter(mailing_failure_reason='')

    def ready_for_mailing(self, timestamp: float | None = None):
        timestamp = time() if timestamp is None else timestamp
        return (
            self
            .exclude_mailing_failed()
            .filter(
                state_machine_locator__state_class_locator='/mailing-queue/',
                state_machine_locator__params__waiting_till__lte=timestamp,
                state_machine_locator__params__expired_after__gte=timestamp,
            )
        )

    def postponed_mailing(self, timestamp: float | None = None):
        timestamp = time() if timestamp is None else timestamp
        return (
            self
            .exclude_mailing_failed()
            .filter(
                state_machine_locator__state_class_locator='/mailing-queue/',
                state_machine_locator__params__waiting_till__gt=timestamp,
                state_machine_locator__params__expired_after__gt=timestamp,
            )
        )

    def annotate_with_tg_username(self):
        from tg_bot.models import Conversation
        related_conversations = Conversation.objects.filter(
            tg_user_id=models.OuterRef('tg_user_id'),
        )

        return self.annotate(
            tg_username=models.Subquery(related_conversations.values('last_update_tg_username')[:1]),
        )

    def annotate_with_tg_chat_id(self):
        from tg_bot.models import Conversation
        related_conversations = Conversation.objects.filter(
            tg_user_id=models.OuterRef('tg_user_id'),
        )

        return self.annotate(
            tg_chat_id=models.Subquery(related_conversations.values('tg_chat_id')[:1]),
        )


class Lead(models.Model):
    tg_user_id = models.BigIntegerField(
        'Id юзера в Tg',
        db_index=True,
        help_text=(
            'Id пользователя Telegram. '
            'Пример значения: <code>123456789</code>.<br>'
            'Чтобы узнать ID пользователя, перешлите сообщение пользователя боту '
            '<a href="https://t.me/userinfobot">@userinfobot</a>.'
        ),
    )

    state_machine_locator = models.JSONField(
        'состояние',
        null=True,
        blank=True,
        help_text=(
            'Локатор состояния, в котором сейчас находится чат с пользователем. Заполняется автоматически. '
            'Используется стейт-машиной.<br>'
            'Пример значения: <code>{"state_class_locator": "/start-menu/"}</code>.<br>'
            'В поле хранится объект JSON в формате локатора из библиотеки '
            '<a href="https://pypi.org/project/yostate/">yostate</a>: '
            'атрибут <code>state_class_locator</code> указывает локатор класса состояния и похож на часть адреса URL, '
            'атрибут <code>params</code> задаёт параметры состояния.'
        ),
    )
    mailing_failure_reason = models.SlugField(
        'код ошибки рассылки',
        db_index=True,
        blank=True,
        help_text='Англоязычный код ошибки по результатам рассылки, например "endless_loop". '
                  'Если поле осталось пустым после рассылки — значит прошло успешно. '
                  'Разрешены те же символы, что бывают внутри slug.',
    )
    mailing_failure_debug_details = models.TextField(
        'описание ошибки рассылки',
        blank=True,
        help_text='Описание ошибки по результатам рассылки. Поле хранит отладочную информацию '
                  'для программиста.',
    )

    objects = LeadQuerySet.as_manager()

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'

    def __str__(self):
        return f'Лид {self.id}'
