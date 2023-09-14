import os
import subprocess
import logging
import time

logger = logging.getLogger('app')


def video2audio(video_path_or_url, audio_filename):
    audio_dir = os.path.dirname(audio_filename)
    os.makedirs(audio_dir, exist_ok=True)
    ffmpeg_cmd = ['ffmpeg', '-i', video_path_or_url, '-vn', audio_filename]
    # GPU运行
    # ffmpeg_cmd = ['ffmpeg', '-hwaccel', 'cuda', '-hwaccel_device', '0', '-i', video_path_or_url, '-vn', audio_filename]
    logger.info(f'提取视频中的音频文件，命令：{" ".join(ffmpeg_cmd)}')
    try:
        start_time = time.time()
        subprocess.run(ffmpeg_cmd, check=True)
        end_time = time.time()
        logger.info(f'提取视频【{audio_filename}】中的音频文件完成，耗时：{(end_time - start_time):.6f}秒')
        return True
    except Exception as e:
        logger.error(f'提取视频中的音频文件失败：{e}')
        return False
