import shutil
import os
import threading
import logging

from modules.util.const_util import FILE_PATH_SEPARATOR
from modules.util import file_util

logger = logging.getLogger('app')


def _merge_file(file_dir, file_name, chunk_dir, files):
    file_full_name = file_dir + FILE_PATH_SEPARATOR + file_name
    if os.path.exists(file_full_name):
        os.remove(file_full_name)
    for file_chunk_name in files:
        with open(chunk_dir + FILE_PATH_SEPARATOR + file_chunk_name, "rb") as in_file, open(
                file_dir + FILE_PATH_SEPARATOR + file_name, "ab") as out_file:
            out_file.write(in_file.read())
        in_file.close()
        out_file.close()
    shutil.rmtree(chunk_dir)


def save_file_chunk(file_chuck, uid, chunk_um):
    file_full_name = file_util.get_chunk_dir() + FILE_PATH_SEPARATOR + uid
    os.makedirs(file_full_name, exist_ok=True)
    with open(file_full_name + FILE_PATH_SEPARATOR + str(chunk_um), "wb") as f:
        shutil.copyfileobj(file_chuck, f)
        f.close()


def merge(uid, file_name, file_size):
    file_suffix = file_util.get_file_suffix(file_name)
    category = file_util.get_file_category(file_suffix)
    file_dir = file_util.get_file_dir(category)
    if file_dir is None:
        logger.error("无效类型")
        return False
    else:
        file_dir = file_dir + FILE_PATH_SEPARATOR + uid
        os.makedirs(file_dir, exist_ok=True)

    chunk_dir = file_util.get_chunk_dir() + FILE_PATH_SEPARATOR + uid
    if not os.path.exists(chunk_dir):
        logger.error("文件夹不存在")
        return False

    files = os.listdir(chunk_dir)
    files = sorted(files, key=lambda f: int(f))

    cur_file_size = 0
    for file_chunk_name in files:
        cur_file_size += os.path.getsize(chunk_dir + FILE_PATH_SEPARATOR + file_chunk_name)
    if cur_file_size != file_size:
        shutil.rmtree(chunk_dir)
        logger.error("合并失败")
        return False

    t1 = threading.Thread(target=_merge_file, args=(file_dir, file_name, chunk_dir, files,))
    t1.start()
    return True


def merge_progress(uid, file_name, file_size):
    file_suffix = file_util.get_file_suffix(file_name)
    category = file_util.get_file_category(file_suffix)
    file_dir = file_util.get_file_dir(category)
    if file_dir is None:
        logger.error("无效类型")
        return False
    file_dir = file_dir + FILE_PATH_SEPARATOR + uid
    file_full_name = file_dir + FILE_PATH_SEPARATOR + file_name
    if os.path.exists(file_full_name):
        cur_file_size = os.path.getsize(file_full_name)
    else:
        cur_file_size = 0
    if file_size == 0:
        return 100.00
    progress = round(cur_file_size * 100 / file_size, 2)
    return progress if progress <= 100 else 100
