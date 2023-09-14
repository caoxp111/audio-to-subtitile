import logging

from faster_whisper import WhisperModel
import time
import torch

logger = logging.getLogger('app')

whisper_model = None
cur_model_name = None


# 效果 large-v2 > medium > small > base > tiny
def load_model(model_name):
    global cur_model_name
    cur_model_name = model_name
    global whisper_model
    whisper_model = None
    start_time = time.time()
    whisper_model = WhisperModel(model_name, device=get_device(), compute_type='float32', download_root='./models')
    end_time = time.time()
    logger.info(f'加载模型完成，耗时：{(end_time - start_time):.6f}秒')


def refresh_model(model_name):
    load_model(model_name)


def get_cur_model_name():
    return cur_model_name


def get_device():
    if torch.cuda.is_available():
        logger.info(
            f'cuda is available, GPU num is {torch.cuda.device_count()}, current device is {torch.cuda.current_device()}, device name is {torch.cuda.get_device_name(0)}')
        return 'cuda'
    else:
        logger.info(
            f'cuda is not available, CPU in use')
        return 'cpu'


def get_model():
    return whisper_model
