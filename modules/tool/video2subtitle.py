import logging
import os
import sys

from modules.tool import audio2subtitle
from modules.util import file_util, ffmpeg_util
from modules.util.const_util import MP3_EXTENSION, FileCategory

logger = logging.getLogger('app')


def generate_subtitle(socketio, namespace, video_filename, srt_file_name, is_save_subtitle, socket_id):
    if not os.path.exists(video_filename):
        return
    audio_filename = (file_util.get_filename_no_ext(video_filename) + MP3_EXTENSION).replace(FileCategory.VIDEO.value,
                                                                                             FileCategory.AUDIO.value)
    encode_video_filename = video_filename.encode(sys.getfilesystemencoding()).decode()
    encode_audio_filename = audio_filename.encode(sys.getfilesystemencoding()).decode()
    run_flag = ffmpeg_util.video2audio(encode_video_filename, encode_audio_filename)
    if not run_flag:
        return
    audio2subtitle.generate_subtitle(socketio, namespace, audio_filename, srt_file_name, is_save_subtitle, socket_id)


def url_generate_subtitle(socketio, namespace, video_url, audio_filename, srt_file_name, is_save_subtitle, socket_id):
    encode_audio_filename = audio_filename.encode(sys.getfilesystemencoding()).decode()
    run_flag = ffmpeg_util.video2audio(video_url, encode_audio_filename)
    if not run_flag:
        return
    audio2subtitle.generate_subtitle(socketio, namespace, audio_filename, srt_file_name, is_save_subtitle, socket_id)
