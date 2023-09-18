from django import forms

from django.contrib import admin

from django_json_widget.widgets import JSONEditorWidget

from tg_bot.models import Conversation


class ConversationAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'state_class_locator': forms.TextInput(attrs={'size': '100'}),
            'state_params': JSONEditorWidget(
                attrs={
                    'style': 'width: 100%; max-width: 1000px; display:inline-block; height:250px;',
                },
            ),
        }


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [
        'tg_user_id',
        'tg_chat_id',
        'tg_username',
        'started_at',
    ]
    date_hierarchy = 'started_at'
    search_fields = [
        'tg_user_id',
        'tg_chat_id',
        'tg_username',
    ]

    form = ConversationAdminForm
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "tg_user_id",
                    "tg_chat_id",
                    "tg_username",
                ],
            },
        ),
        (
            "Стейт-машина",
            {
                "fields": ["state_class_locator", "state_params"],
            },
        ),
        (
            "Дополнительно",
            {
                "classes": ["collapse"],
                "fields": ["started_at"],
            },
        ),
    ]
