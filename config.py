import codecs
import json
import os

import env
from bean.config_bean import ConfigBean

def write_config(config):
    try:
        # if config.get(key) is None or config[key] != value or len(config[key]) != 0:
        #     config[key] = value
        with open(env.getConfigPath(), 'w') as writeFile:
            json.dump(config, writeFile)
    except Exception as e:
        pass

def read_config() -> ConfigBean:
    if not os.path.exists(env.getConfigPath()):
        with codecs.open(env.getConfigPath(), 'a+', encoding='utf-8') as f:
            f.write("{}")
            return ''
    try:
        with open(env.getConfigPath()) as f:
            config = json.load(f)
            bean = ConfigBean()
            bean.host = config.get('host')
            bean.port = config.get('port')
            bean.task_path = config.get('task_path')
            return bean
    except Exception as e:
        pass
