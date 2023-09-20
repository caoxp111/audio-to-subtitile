import logging
import time
import os

from modules.util.const_util import ResponseEvent
from modules.tool import load
from modules.util import time_util, response_util, url_util

logger = logging.getLogger('app')


def generate_subtitle(socketio, namespace, audio_filename, srt_file_name, is_save_subtitle, socket_id):
    if not os.path.exists(audio_filename):
        return
    whisper_model = load.whisper_model
    if whisper_model is None:
        logger.error('模型文件未加载')
        return
    start_time = time.time()
    segments, info = whisper_model.transcribe(audio_filename, beam_size=5, vad_filter=True)
    for segment in segments:
        start_ts = time_util.trans_ts(segment.start)
        end_ts = time_util.trans_ts(segment.end)
        text = segment.text
        if is_save_subtitle:
            srt_dir = os.path.dirname(srt_file_name)
            os.makedirs(srt_dir, exist_ok=True)
            with open(srt_file_name, 'a', encoding='utf-8') as file:
                file.write(f'{segment.id}\n{start_ts} --> {end_ts}\n{text}\n\n')
        text_line = f'[{start_ts} -> {end_ts}] {text}'
        response_util.ws_response(socketio, namespace, ResponseEvent.SUBTITLE.value, socket_id,
                                  {'status': 1, 'text': text_line,
                                   'progress': round(segment.end * 100 / info.duration, 2)})
    end_time = time.time()
    spend_time = round(end_time - start_time, 6)
    logger.info(f'文件【{audio_filename}】生成字幕完成，耗时：{spend_time}秒')
    response_util.ws_response(socketio, namespace, ResponseEvent.SUBTITLE.value, socket_id,
                              {'status': 2, 'spend': spend_time, 'progress': 100, 'srt_path': srt_file_name[1:]})


def url_generate_subtitle(socketio, namespace, audio_url, audio_filename, srt_file_name, is_save_subtitle, socket_id):
    audio_dir = os.path.dirname(audio_filename)
    os.makedirs(audio_dir, exist_ok=True)
    download_flag = url_util.download(audio_url, audio_filename)
    if not download_flag:
        return
    generate_subtitle(socketio, namespace, audio_filename, srt_file_name, is_save_subtitle, socket_id)
