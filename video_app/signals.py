import os
import shutil
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from video_app.models import VideoModel
from video_app.tasks import convert_task

va_logger = logging.getLogger('video_app')

@receiver(post_save, sender= VideoModel)
def on_video_save(sender, instance, **kwargs):

    if VideoModel.CACHE_KEY in cache:
        cache.delete(VideoModel.CACHE_KEY)

    va_logger.info('Video file saved - {}'.format(
        instance.video_file_path
    ))
    convert_task.delay(
        id= instance.id,
        file_path= instance.video_file_path.path
    )
    
@receiver(post_delete, sender=VideoModel)
def delete_media(sender, instance, **kwargs):
    
    if VideoModel.CACHE_KEY in cache:
        cache.delete(VideoModel.CACHE_KEY)

    if (instance.video_file_path and 
        os.path.isfile(instance.video_file_path.path)):
        try :
            dir_path= instance.video_file_path.path
            dir_path = dir_path.rsplit(os.sep, 1)[0]
            shutil.rmtree(dir_path, ignore_errors=True)

        except OSError as e:
            va_logger.error("Error: %s : %s" % (dir_path, e.strerror))


    va_logger.info('Video Deleted - {}'.format(
        instance.video_file_path.path
    ))