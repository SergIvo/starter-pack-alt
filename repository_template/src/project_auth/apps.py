from django.apps import AppConfig


class UserAccessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_auth'
    label = 'project_auth'
    verbose_name = 'Аутентификация'
