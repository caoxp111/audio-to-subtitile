from flask import request, Blueprint
import logging

from modules.tool import load
from modules.util import response_util

logger = logging.getLogger('app')

model_route = Blueprint('model_route', __name__)


@model_route.route('/model/refresh', methods=['POST'])
def model_refresh():
    params = request.get_json()
    model_name = params['modelName']
    logger.info(f'model_name= {model_name}')
    load.refresh_model(model_name)
    return response_util.success_response(None)


@model_route.route('/model/getCurModelName', methods=['GET'])
def get_cur_model_name():
    return response_util.success_response(load.get_cur_model_name())
