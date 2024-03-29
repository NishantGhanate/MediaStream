import os
import shutil
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from media_stream.utils.caching import clear_cache
from video_app.models import TvChannelModel, VideoModel

from video_app.tasks import convert_task

va_logger = logging.getLogger('video_app')


@receiver(post_save, sender= TvChannelModel)
def on_tvchannel_save(sender, instance, **kwargs):
    clear_cache(model_instance= instance)

@receiver(post_delete, sender= TvChannelModel)
def on_tvchannel_delete(sender, instance, **kwargs):
    clear_cache(model_instance= instance)
    
@receiver(post_save, sender= VideoModel)
def on_video_save(sender, instance, **kwargs):
    va_logger.info('Video file saved - {}'.format(
        instance.video_file_path
    ))
    clear_cache(model_instance= instance)
    convert_task.delay(
        id= instance.id,
        file_path= instance.video_file_path.path
    )
    
@receiver(post_delete, sender=VideoModel)
def delete_media(sender, instance, **kwargs):

    clear_cache(model_instance= instance)
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
