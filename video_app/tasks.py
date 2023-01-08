import os
import shutil
import pathlib
import logging
import celery

from datetime import datetime
from celery import shared_task
# from django_celery_results.models import TaskResult
from django.core.cache import cache

from video_app.video_convert import mp4_hls
from video_app.models import Status, VideoModel
from media_stream.utils.custom_exceptions import VideoProcessFailed

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
PROCESSED_PATH = pathlib.Path(settings.BASE_DIR, 'processed') 

vc_logger = logging.getLogger('video_convert')

class MyBaseClassForTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        - exc (Exception) - The exception raised by the task.
        - args (Tuple) - Original arguments for the task that failed.
        - kwargs (Dict) - Original keyword arguments for the task that failed.
        """
        
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        print('{0!r} success:'.format(task_id))
        print(retval)
        print(args, kwargs)

@shared_task(name= 'video_app.tasks.factorial', base=MyBaseClassForTask)
def factorial(n):
    message = '{n} factorial = {fact}!'
    if n <= 1:
        return message.format(n= n, fact= n)

    fact = 1
    key_check ='factorial_{}'.format(n)
    if key_check in cache:
        fact = cache.get(key_check)
        print('Value found in cahce')
        return message.format(n=n, fact=fact)

    for i in range(1, n+1):
        fact *= i

    cache.set(key_check, fact, timeout=CACHE_TTL)   
    return message.format(n= n, fact= fact)

class VideoConverTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        vc_logger.error('{0!r} failed: {1!r}'.format(task_id, exc))
        # TaskResult.objects.filter(task_id=task_id).update(traceback = '')

    def on_success(self, retval, task_id, args, kwargs):
        vc_logger.info(f"success : {kwargs['id']} - {kwargs['file_path']}")
        # move media file 
        file_name =  kwargs['file_path'].rsplit(os.sep, 1)[1]
        new_path = os.path.join(PROCESSED_PATH, file_name)
        shutil.move(src= kwargs['file_path'], dst= new_path)
        

@shared_task(base= VideoConverTask)
def convert_task(id, file_path):
    vc_logger.info(f'video id = {id}, Task received - {file_path}')
    # Before process call 
    before = datetime.now()
    result = mp4_hls(file_path= file_path)
    time_took = str(datetime.now() - before)
    vc_logger.info(f'result = {result}')
    
    if 'error' in result:
        VideoModel.objects.filter(pk=id).update(
            processing_status = Status.FAILED
        )
        raise VideoProcessFailed(
            message= result['error']
        )

    VideoModel.objects.filter(pk=id).update(
        processing_status = Status.FINISHED,
        processing_completed = time_took,
        **result
    )

    return result
