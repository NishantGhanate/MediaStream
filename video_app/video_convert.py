from asyncio.log import logger
import sys
import datetime
import logging
import traceback
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

from video_app.models import VideoModel

video_logger = logging.getLogger('video_convert')

_480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
_720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
_1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
_2k    = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
_4k    = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

def monitor(ffmpeg, duration, time_, time_left, process):
    """
    Handling proccess.

    Examples:
    1. Logging or printing ffmpeg command
    logging.info(ffmpeg) or print(ffmpeg)

    2. Handling Process object
    if "something happened":
        process.terminate()

    3. Email someone to inform about the time of finishing process
    if time_left > 3600 and not already_send:  # if it takes more than one hour and you have not emailed them already
        ready_time = time_left + time.time()
        Email.send(
            email='someone@somedomain.com',
            subject='Your video will be ready by %s' % datetime.timedelta(seconds=ready_time),
            message='Your video takes more than %s hour(s) ...' % round(time_left / 3600)
        )
       already_send = True

    4. Create a socket connection and show a progress bar(or other parameters) to your users
    Socket.broadcast(
        address=127.0.0.1
        port=5050
        data={
            percentage = per,
            time_left = datetime.timedelta(seconds=int(time_left))
        }
    )

    :param ffmpeg: ffmpeg command line
    :param duration: duration of the video
    :param time_: current time of transcoded video
    :param time_left: seconds left to finish the video process
    :param process: subprocess object
    :return: None
    """
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]" %
        (
            per, 
            datetime.timedelta(seconds=int(time_left)),
            '#' * per, 
            '-' * (100 - per)
        )
    )
    sys.stdout.flush()

def mp4_hls(id , file_path):
    """
    Takes two params for video model instance
    @id : int
    @file_path : str

    """
    converted = False
    try :
        video_logger.info('Starting m3u8 file conversion for : {}'.format(file_path))
        # video = ffmpeg_streaming.input(file_path)
        # hls = video.hls(Formats.h264())
        # hls.representations(_480p, _720p, _1080p)
        # hls.output('D:\Projects\django-hls\media\BigBuckBunny_hls.m3u8')
        converted = True
    except :
        video_logger.error(traceback.format_exc())
    
    return converted
    
    