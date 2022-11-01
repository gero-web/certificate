from django.apps import AppConfig
from django.db.models.signals import post_delete


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        from app.signals.delimageSignal import auto_delete_file_on_delete
        post_delete.connect(auto_delete_file_on_delete, sender=self)


