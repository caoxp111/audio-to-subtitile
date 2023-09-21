from flask import request
from flask_socketio import Namespace
import threading
import logging

from modules.tool import audio2subtitle, video2subtitle
from modules.util.const_util import FileCategory, FILE_PATH_SEPARATOR, SRT_EXTENSION, MP3_EXTENSION, MP4_EXTENSION
from modules.util import file_util, url_util

logger = logging.getLogger('app')

socket_id_set = set()


class ProcessNamespace(Namespace):

    def __init__(self, namespace, socketio):
        super().__init__(namespace)
        self.socketio = socketio

    def audio_extract_subtitle(self, audio_path, srt_path, socket_id):
        threading.Thread(target=audio2subtitle.generate_subtitle,
                         args=(self.socketio, self.namespace, audio_path, srt_path, True, socket_id,)).start()

    def video_extract_subtitle(self, video_path, srt_path, socket_id):
        threading.Thread(target=video2subtitle.generate_subtitle,
                         args=(self.socketio, self.namespace, video_path, srt_path, True, socket_id,)).start()

    def audio_url_extract_subtitle(self, audio_url, audio_path, srt_path, socket_id):
        threading.Thread(target=audio2subtitle.url_generate_subtitle,
                         args=(
                             self.socketio, self.namespace, audio_url, audio_path, srt_path, True, socket_id,)).start()

    def video_url_extract_subtitle(self, video_url, video_path, audio_path, srt_path, socket_id):
        threading.Thread(target=video2subtitle.url_generate_subtitle, args=(
            self.socketio, self.namespace, video_url, video_path, audio_path, srt_path, True, socket_id,)).start()

    def on_connect(self):
        socket_id = request.sid
        socket_id_set.add(socket_id)
        logger.info(f'socket_id: {socket_id} connected, connect num: {len(socket_id_set)}')

    def on_disconnect(self):
        socket_id = request.sid
        socket_id_set.remove(socket_id)
        logger.info(f'socket_id: {socket_id} disconnect, connect num: {len(socket_id_set)}')

    def on_submit_file(self, params):
        socket_id = request.sid
        uid = params['uid']
        file_name = params['fileName']
        logger.info(f'提交任务参数，socket_id: {socket_id}, uid: {uid}, file_name: {file_name}')
        file_suffix = file_util.get_file_suffix(file_name)
        category = file_util.get_file_category(file_suffix)
        if FileCategory.VIDEO == category:
            file_dir = file_util.get_file_dir(category)
            video_path = file_dir + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name
            file_name_no_ext = file_util.get_filename_no_ext(file_name)
            srt_path = file_util.get_out_puts_dir() + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name_no_ext + SRT_EXTENSION
            # 先转音频，再生成字幕
            self.video_extract_subtitle(video_path, srt_path, socket_id, )
        elif FileCategory.AUDIO == category:
            file_dir = file_util.get_file_dir(category)
            audio_path = file_dir + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name
            file_name_no_ext = file_util.get_filename_no_ext(file_name)
            srt_path = file_util.get_out_puts_dir() + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name_no_ext + SRT_EXTENSION
            # 直接生成字幕
            self.audio_extract_subtitle(audio_path, srt_path, socket_id, )
        elif FileCategory.PDF == category:
            logger.info('pdf')
        else:
            logger.error("无效文件")
            return

    def on_submit_link(self, params):
        socket_id = request.sid
        uid = params['uid']
        file_url = params['fileUrl']
        logger.info(f'提交任务参数，socket_id: {socket_id}, uid: {uid}, file_url: {file_url}')
        category, file_name = url_util.get_link_file_category_and_filename(file_url)
        if FileCategory.VIDEO == category:
            video_file_dir = file_util.get_file_dir(FileCategory.VIDEO)
            audio_file_dir = file_util.get_file_dir(FileCategory.AUDIO)
            file_name_no_ext = file_util.get_filename_no_ext(file_name)
            video_path = video_file_dir + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name_no_ext + MP4_EXTENSION
            audio_path = audio_file_dir + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name_no_ext + MP3_EXTENSION
            srt_path = file_util.get_out_puts_dir() + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name_no_ext + SRT_EXTENSION
            # 先转音频，再生成字幕
            self.video_url_extract_subtitle(file_url, video_path, audio_path, srt_path, socket_id, )
        elif FileCategory.AUDIO == category:
            file_dir = file_util.get_file_dir(category)
            audio_path = file_dir + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name
            file_name_no_ext = file_util.get_filename_no_ext(file_name)
            srt_path = file_util.get_out_puts_dir() + FILE_PATH_SEPARATOR + uid + FILE_PATH_SEPARATOR + file_name_no_ext + SRT_EXTENSION
            self.audio_url_extract_subtitle(file_url, audio_path, srt_path, socket_id, )
        elif FileCategory.PDF == category:
            logger.info('pdf')
        else:
            logger.error("无效文件")
            return


def handler(socketio):
    return ProcessNamespace('/process', socketio)
