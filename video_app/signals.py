import os
import shutil
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.core.management import call_command

from video_app.models import TvChannelModel, VideoModel
from video_app.tasks import convert_task

va_logger = logging.getLogger('video_app')



@receiver(post_save, sender= VideoModel)
def on_video_save(sender, instance, **kwargs):
    va_logger.info('Video file saved - {}'.format(
        instance.video_file_path
    ))
    call_command("clear_cache", model= ("VideoModel", ))
    convert_task.delay(
        id= instance.id,
        file_path= instance.video_file_path.path
    )
    
@receiver(post_delete, sender=VideoModel)
def delete_media(sender, instance, **kwargs):

    call_command("clear_cache", model= ("VideoModel", ))
    
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

@receiver(post_save, sender= TvChannelModel)
def on_tvchannel_save(sender, instance, **kwargs):
    call_command("clear_cache", model= ("TvChannelModel", ))

@receiver(post_delete, sender= TvChannelModel)
def on_tvchannel_delete(sender, instance, **kwargs):
    call_command("clear_cache", model= ("TvChannelModel", ))
    