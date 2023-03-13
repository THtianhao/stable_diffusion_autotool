import traceback

from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets

import api.feishu_api
from api.feishu_api import *
from bean.task_bean import TasksBean
from config import *
from log_utils import LogUtils
from task_thread import TaskThread
from ui.main import Ui_MainWindow

class MainWindow(Ui_MainWindow, QMainWindow):
    printSignal = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        try:
            self.setupUi(self)
            self.thread: TaskThread = None
            self.config = ConfigBean()
            self.file_tag = "chrome_config"
            self.saveConfig.clicked.connect(self.save_config)
            self.openTaskPath.clicked.connect(self.open_task_path)
            self.startTask.clicked.connect(self.start_tasks)
            self.stopTask.clicked.connect(self.stop_tasks)
            self.getFeishuCode.clicked.connect(self.feishu_code)
            self.log_utils = LogUtils('AutoTool', self.printSignal)
            self.read_config()
            self.printSignal.connect(self.print_log)
        except Exception as e:
            self.log_utils.e(traceback.format_exc())

    def save_config(self):
        write_config(self.config.__dict__)

    def read_config(self):
        self.config = read_config()
        if self.config is None:
            return
        self.host.setText('' if self.config.host is None else self.config.host)
        self.port.setText('' if self.config.port is None else self.config.port)
        self.feishuCode.setText('' if self.config.feishu_code is None else self.config.feishu_code)
        self.taskPath.setText('' if self.config.task_path is None else self.config.task_path)
        if self.config.upload_feishu is not None and self.config.upload_feishu == 1:
            self.uploadFeishu.setChecked(True)
        else:
            self.uploadFeishuNot.setChecked(True)
        if self.config.operation is not None and self.config.operation == 2:
            self.merge.setChecked(True)
        else:
            self.mergeAndT2I.setChecked(True)

    def feishu_code(self):
        QDesktopServices.openUrl(QUrl("https://open.feishu.cn/open-apis/authen/v1/index?app_id=cli_a483ea8b94e3100e&redirect_uri=http://127.0.0.1"))

    def checkConfig(self) -> bool:
        self.config.operation = 2 if self.mergeAndT2I.isChecked() else 1
        self.config.upload_feishu = 1 if self.uploadFeishu.isChecked() else 0
        self.config.host = self.host.text()
        self.config.port = self.port.text()
        self.config.feishu_code = self.feishuCode.text()
        self.config.task_path = self.taskPath.text()
        if self.config.task_path is None or self.config.host is None or self.config.port is None \
                or self.config.task_path == '' or self.config.host == '' or self.config.port == '':
            self.log_utils.e("Please configuration the host port and tasks first")
            return False
        return True

    def start_tasks(self):
        if not self.checkConfig():
            return
        self.save_config()
        try:
            tasks = self.read_task()
            if tasks == '':
                return
            tasks_bean = TasksBean()
            tasks_bean.__dict__ = tasks
            self.thread = TaskThread(self, tasks_bean, self.config)
            print("ready to start")
            self.thread.start()
        except:
            self.log_utils.e(traceback.format_exc())

    def stop_tasks(self):
        if self.thread is None:
            self.log_utils.e("No task running")
        self.thread.stop()

    def print_log(self, log):
        self.logPanel.append(log)
        self.logPanel.ensureCursorVisible()

    def read_task(self) -> str:
        if not os.path.exists(self.config.task_path):
            self.print_log("tasks file not exist")
            return ''
        try:
            with open(self.config.task_path) as f:
                return json.load(f)
        except Exception as e:
            pass

    def open_task_path(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件夹", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        self.taskPath.setText(fileName)
        write_config(self.config)
