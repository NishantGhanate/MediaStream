import os
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from video_app.models import VideoModel
from video_app.tasks import convert_task

logger = logging.getLogger('videp_app')

@receiver(post_save, sender= VideoModel)
def on_video_save(sender, **kwargs):
    logger.info('Video file saved - {}'.format(
        kwargs['instance'].video_file_name
    ))
    
    convert_task.delay(
        id= kwargs['instance'].id,
        file_path= kwargs['instance'].video_file_name.path
    )
    

@receiver(post_delete, sender=VideoModel)
def delete_media(sender, instance, **kwargs):
    if instance.video_thumbnail:
        if os.path.isfile(instance.video_thumbnail.path):
            os.remove(instance.video_thumbnail.path)
    
    if instance.video_file_name:
        if os.path.isfile(instance.video_file_name.path):
            os.remove(instance.video_file_name.path)