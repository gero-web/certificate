import os
from app.models import Component
from django.dispatch import receiver
from django.db.models.signals import post_delete


@receiver(post_delete, sender=Component)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
        if instance.file:
        if os.path.isfile(instance.image.path):
            os.remove(instance.file.path)
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


