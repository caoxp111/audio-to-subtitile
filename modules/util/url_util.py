import logging
import re
from urllib.parse import unquote

import requests

from modules.util import random_util
from modules.util.const_util import FileCategory, MP4_EXTENSION, MP3_EXTENSION, PDF_EXTENSION

logger = logging.getLogger('app')


def get_link_response(file_url):
    try:
        response = requests.head(file_url)
        if response.status_code == 200:
            return response
        else:
            logging.error(f"请求链接失败：{file_url}")
            return None
    except Exception as e:
        logging.error(f"无效链接：{file_url}，异常：{e}")
        return None


def get_link_file_category_and_filename(file_url):
    response = get_link_response(file_url)
    if response is None:
        return None, None
    return get_file_category_and_filename(response.headers)


def get_file_category_and_filename(headers):
    content_type = headers.get('Content-Type')
    if content_type is None:
        return None, None
    if content_type.startswith('video'):
        return FileCategory.VIDEO, get_filename(headers, MP4_EXTENSION)
    elif content_type.startswith('audio'):
        return FileCategory.AUDIO, get_filename(headers, MP3_EXTENSION)
    elif content_type.startswith('pdf'):
        return FileCategory.PDF, get_filename(headers, PDF_EXTENSION)
    else:
        return None, None


def get_filename(headers, file_extension):
    content_disposition = headers.get('Content-Disposition')
    if content_disposition:
        filename = re.findall('filename="(.+)"', content_disposition)
        if filename:
            filename = unquote(filename[0])
        else:
            filename = random_util.get_uuid() + file_extension
    else:
        filename = random_util.get_uuid() + file_extension
    return filename


def download(file_url, file_name):
    try:
        response = requests.get(file_url)
        if response.status_code != 200:
            logging.error(f"请求链接失败：{file_url}")
            return False
    except Exception as e:
        logging.error(f"无效链接：{file_url}，异常：{e}")
        return False
    with open(file_name, "wb") as f:
        f.write(response.content)
    return True
