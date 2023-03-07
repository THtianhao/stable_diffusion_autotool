import codecs
import json
import os

import env

config: json = {}
host_flag = "host"
port_flag = "port"
tasks_flag = "task"
def save_config(self):
    host = self.host.text()
    port = self.port.text()
    task = self.taskPath.text()
    if host != '':
        self.write_config(self.host_flag, host)
    if port != '':
        self.write_config(self.port_flag, port)
    if task != '':
        self.write_config(self.tasks_flag, task)

def write_config(key, value):
    try:
        if config.get(key) is None or config[key] != value or len(config[key]) != 0:
            config[key] = value
            with open(env.getConfigPath(), 'w') as writeFile:
                json.dump(config, writeFile)
    except Exception as e:
        print("json保存错误!" + str(e))


def read_config():
    if not os.path.exists(env.getConfigPath()):
        with codecs.open(env.getConfigPath(), 'a+', encoding='utf-8') as f:
            f.write("{}")
            return
    try:
        with open(env.getConfigPath()) as f:
            config = json.load(f)

    except Exception as e:
        print(e)