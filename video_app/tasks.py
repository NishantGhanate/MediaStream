import logging
import celery
from celery import shared_task

from video_app.video_convert import mp4_hls
from video_app.models import VideoModel, Status

video_logger = logging.getLogger('video_convert')

class MyBaseClassForTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        - exc (Exception) - The exception raised by the task.
        - args (Tuple) - Original arguments for the task that failed.
        - kwargs (Dict) - Original keyword arguments for the task that failed.
        """
        
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        print('WOW factorial done ')
        print('{0!r} success:'.format(task_id))
        print(retval)
        print(args, kwargs)

@shared_task(name= 'video_app.tasks.factorial', base=MyBaseClassForTask)
def factorial(n):
    message = '{n} factorial = {fact}!'
    if n <= 1:
        return message.format(n= n, fact= n)

    fact = 1
    for i in range(1, n+1):
        fact *= i

    return message.format(n= n, fact= fact)


class VideoConverTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        video_logger.error('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        video_logger.info('success : {}'.format(kwargs['file_path']))

        print(kwargs['id'], kwargs['file_path'])

@shared_task(base= VideoConverTask)
def convert_task(id, file_path):
    video_logger.info('Task received - {}'.format(file_path))
    result = mp4_hls(id= id, file_path= file_path)
    if not result:
        raise Exception()
    return result
