import os
import shutil
import logging
import datetime

from modules.util import file_util
from modules.util.const_util import FileCategory, FILE_PATH_SEPARATOR

logger = logging.getLogger('app')


def delete_record(date_dir):
    video_file_date_dir = file_util.get_file_dir(FileCategory.VIDEO) + FILE_PATH_SEPARATOR + date_dir
    audio_file_date_dir = file_util.get_file_dir(FileCategory.AUDIO) + FILE_PATH_SEPARATOR + date_dir
    chunk_file_date_dir = file_util.get_chunk_dir() + FILE_PATH_SEPARATOR + date_dir
    out_puts_file_date_dir = file_util.get_out_puts_dir() + FILE_PATH_SEPARATOR + date_dir
    if os.path.exists(video_file_date_dir):
        shutil.rmtree(video_file_date_dir)
    if os.path.exists(audio_file_date_dir):
        shutil.rmtree(audio_file_date_dir)
    if os.path.exists(chunk_file_date_dir):
        shutil.rmtree(chunk_file_date_dir)
    if os.path.exists(out_puts_file_date_dir):
        shutil.rmtree(out_puts_file_date_dir)
    logger.info(
        f'删除视频目录：{video_file_date_dir}，音频目录：{audio_file_date_dir}，分片目录：{chunk_file_date_dir}，输出目录：{out_puts_file_date_dir}完成')


def delete_record_scheduler():
    ten_days_ago_str = (datetime.datetime.today() - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    delete_record(ten_days_ago_str)
