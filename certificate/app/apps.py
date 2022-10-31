from django.apps import AppConfig
<<<<<<< HEAD

=======
from django.db.models.signals import post_delete
>>>>>>> 5b4bdfc7f47bc7933ff73f8b9c316895d66d24e3

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
<<<<<<< HEAD
=======

    def ready(self):
        from app.signals.delimageSignal import auto_delete_file_on_delete
        post_delete.connect(auto_delete_file_on_delete, sender=self)

>>>>>>> 5b4bdfc7f47bc7933ff73f8b9c316895d66d24e3
