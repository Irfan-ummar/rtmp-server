from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Camera
from .utils import start_stream, stop_stream

@receiver(post_save, sender=Camera)
def camera_post_save(sender, instance, created, **kwargs):
    """
    Signal handler that runs when a Camera model is saved
    
    If a camera is newly created and active=True, start streaming
    """
    if created and instance.active:
        start_stream(instance)

@receiver(post_delete, sender=Camera)
def camera_post_delete(sender, instance, **kwargs):
    """
    Signal handler that runs when a Camera model is deleted
    
    Stop streaming for deleted cameras
    """
    stop_stream(instance) 