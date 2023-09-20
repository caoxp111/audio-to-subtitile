from flask import request, Blueprint, send_file
import logging
import os

from modules.upload import upload
from modules.util import response_util

logger = logging.getLogger('app')

file_route = Blueprint('file_route', __name__)


@file_route.route('/file/uploadChunk', methods=['POST'])
def file_upload_chunk():
    file_chuck = request.files['fileChuck']
    uid = request.form['uid']
    chunk_num = request.form['chunkNum']
    logger.info(f'uid= {uid}, chunkNum= {chunk_num}')
    flag = upload.save_file_chunk(file_chuck, uid, chunk_num)
    if flag:
        return response_util.success_response(None)
    else:
        return response_util.failed_response1("上传分片失败")


@file_route.route('/file/merge', methods=['POST'])
def file_merge():
    params = request.get_json()
    uid = params['uid']
    file_name = params['fileName']
    file_size = params['fileSize']
    logger.info(f'uid= {uid}, fileName= {file_name}, fileSize={file_size}')
    flag = upload.merge(uid, file_name, file_size)
    if flag:
        return response_util.success_response(None)
    else:
        return response_util.failed_response1("合并分片失败")


@file_route.route('/file/merge/progress', methods=['POST'])
def file_merge_progress():
    params = request.get_json()
    uid = params['uid']
    file_name = params['fileName']
    file_size = params['fileSize']
    logger.info(f'uid= {uid}, fileName= {file_name}, fileSize={file_size}')
    progress = upload.merge_progress(uid, file_name, file_size)
    return response_util.success_response({"progress": progress})


@file_route.route('/file/<path:filename>')
def download_file(filename):
    file_path = './' + filename
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return response_util.failed_response1('未找到对应文件')
    return send_file(file_path)
