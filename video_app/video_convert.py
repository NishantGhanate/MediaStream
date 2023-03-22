import os
import sys
import datetime
import logging
import traceback
import ffmpeg_streaming
from ffmpeg_streaming import (
    Formats, Bitrate, Representation, Size,
    FFProbe
)


vc_logger = logging.getLogger('video_convert')

# _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
_720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
_1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
_2k    = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
_4k    = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

RESOLUTIONS = (_720p, _1080p)

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

def mp4_hls(file_path):
    """
    Convert the given mp4 to hls

    @params:
        file_path - str 
    
    @rtype :
        meta_data - dict

    """
    meta_data = {}
    try :
        vc_logger.info('Starting m3u8 file conversion for : {}'.format(file_path))
        file_name = file_path.rsplit(os.sep, 1)
       
        ffprobe = FFProbe(file_path) 
        video_format = ffprobe.format()
        first_video = ffprobe.streams().video()
        first_audio = ffprobe.streams().audio()

        # duration: 00:00:10.496
        # size: 290k - 2.9mb
        dimension = '{}x{}'.format(
            first_video.get('width', "-"),
            first_video.get('height', "-")
        )
        file_size = round(int(video_format.get('size', 0)) / 1024)
        # TODO : add auto fie size formatter 
        file_size = '{}k'.format(file_size)
        duration = datetime.timedelta(
            seconds=float(video_format.get('duration', 0))
        )
        meta_data = {
            'duration' : str(duration),
            'file_size' : file_size,
            'dimension' : dimension,
            'display_aspect_ratio' : first_video.get('display_aspect_ratio', '-'),
            'overall_bit_rate' : round(int(video_format.get('bit_rate', 0)) / 1024),
            'video_bitrate' : round(int(first_video.get('bit_rate', 0)) / 1024),
            'audio_bitrate' : round(int(first_audio.get('bit_rate', 0)) / 1024)   
        }

        # Remove file extension 
        m3u8_name = file_name[1].rsplit('.', 1)[0]
        m3u8_name = f'{m3u8_name}_hls.m3u8'

        # Create new file path for it
        m3u8_path = os.path.join(file_name[0], m3u8_name)
        video = ffmpeg_streaming.input(file_path)
        hls = video.hls(Formats.h264())
        hls.representations(_720p, _1080p)
        hls.output(m3u8_path, monitor= monitor)
        
        # since we are storing in project/media on win it will be projects\\media
        converted_path = m3u8_path.split('media')[1]
        if '\\' in converted_path:
            converted_path = converted_path.replace('\\', '/')

        meta_data['m3u8_file_path'] = converted_path
        
    except :
        vc_logger.error(traceback.format_exc())
        meta_data = {
            'error' : str(traceback.format_exc())
        }
        
    return meta_data
    
    