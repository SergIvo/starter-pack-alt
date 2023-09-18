from django.contrib import admin
from user_access.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
    ]
    search_fields = [
        'id',
        'first_name',
        'last_name',
        'email',
    ]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    'first_name',
                    'last_name',
                    'email',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                ],
            },
        ),
    ]
