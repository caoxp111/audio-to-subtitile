import yaml
import os
import logging.config

env_conf = None


def env_config(env_config_file):
    env = os.environ.get("env", "dev")
    print("当前环境是：" + env)
    global env_conf
    if env_conf is None:
        with open(env_config_file, 'rb') as f:
            all_conf = yaml.safe_load(f.read())
        env_conf = all_conf[env]
    return env_conf


def log_config(log_config_file):
    with open(file=log_config_file, mode='rt', encoding="utf-8") as f:
        log_conf = yaml.load(stream=f, Loader=yaml.FullLoader)
    logging.config.dictConfig(config=log_conf)
