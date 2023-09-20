import conf
import os

from modules.util.const_util import FileCategory, FILE_PATH_SEPARATOR


def get_file_dir(category: FileCategory):
    if category is None:
        return None
    else:
        return conf.env_conf['upload_root_dir'] + FILE_PATH_SEPARATOR + category.value


def get_file_category(file_suffix):
    file_category = conf.env_conf['file_category']
    video_suffix = file_category['video_suffix']
    audio_suffix = file_category['audio_suffix']
    pdf_suffix = file_category['pdf_suffix']
    if file_suffix in video_suffix:
        return FileCategory.VIDEO
    elif file_suffix in audio_suffix:
        return FileCategory.AUDIO
    elif file_suffix in pdf_suffix:
        return FileCategory.PDF
    else:
        return None


def get_file_suffix(filename):
    return os.path.splitext(filename)[1][1:]


def get_filename_no_ext(filename):
    return os.path.splitext(filename)[0]


def get_chunk_dir():
    return conf.env_conf['upload_root_dir'] + conf.env_conf['chunk_dir']


def get_out_puts_dir():
    return conf.env_conf['out_puts_dir']


def get_upload_root_dir():
    return conf.env_conf['upload_root_dir']
