from flask import Flask
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler

import conf
from modules.route import index, file, process, model
from modules.tool import load
from modules.scheduler import history_record_scheduler

app = Flask(__name__)
# app.config['SECRET_KEY'] = '123456'


socketio = SocketIO(app, cors_allowed_origins='*')


def add_scheduler():
    scheduler = BackgroundScheduler()
    # 定时删除以前的文件记录，每天0点0分30秒执行
    scheduler.add_job(func=history_record_scheduler.delete_record_scheduler, trigger='cron', hour=0, minute=0,
                      second=30)
    scheduler.start()


def add_routes():
    # http
    app.register_blueprint(index.index_route)
    app.register_blueprint(file.file_route)
    app.register_blueprint(model.model_route)

    # websocket
    socketio.on_namespace(process.handler(socketio))


if __name__ == '__main__':
    conf.env_config('conf.yaml')
    conf.log_config('logging.yaml')
    add_routes()
    add_scheduler()
    load.load_model('tiny')
    # audio2subtitle.generate_subtitle(
    #     "./upload/audio/2023-08-25/3e0a6d30434111eea41a4b35c6cc4059/nos_mp4_2014_07_15_513024_sd.mp3", True,
    #     "./out-puts/2023-08-25/3e0a6d30434111eea41a4b35c6cc4059/nos_mp4_2014_07_15_513024_sd.srt")
    #     allow_unsafe_werkzeug=True,
    socketio.run(app, host='0.0.0.0', port=8181)
