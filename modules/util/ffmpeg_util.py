import os
import subprocess
import logging
import time

logger = logging.getLogger('app')


def video2audio(video_path_or_url, audio_filename):
    audio_dir = os.path.dirname(audio_filename)
    os.makedirs(audio_dir, exist_ok=True)
    # 提取为16k Hz，单通道音频
    ffmpeg_cmd = ['ffmpeg', '-y', '-i', video_path_or_url, '-vn', '-ar', '16000', '-ac', '1', audio_filename]
    # GPU运行
    # ffmpeg_cmd = ['ffmpeg', '-hwaccel', 'cuda', '-hwaccel_device', '0', '-i', video_path_or_url, '-vn', audio_filename]
    logger.info(f'提取视频中的音频文件，命令：{" ".join(ffmpeg_cmd)}')
    try:
        start_time = time.time()
        completed_process = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                           check=False)
        end_time = time.time()
        if completed_process.returncode != 0:
            logger.error(f'提取视频中的音频文件失败：\n{completed_process.stdout}')
            return False
        else:
            logger.info(f'提取视频【{video_path_or_url}】中的音频文件【{audio_filename}】完成，耗时：{(end_time - start_time):.6f}秒')
            return True
    except Exception as e:
        logger.error(f'提取视频中的音频文件失败：{e}')
        return False
