import traceback

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
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
            self.thread = None
            self.config: ConfigBean = ConfigBean()
            self.file_tag = "chrome_config"
            self.saveConfig.clicked.connect(self.save_config)
            self.openTaskPath.clicked.connect(self.open_task_path)
            self.startTask.clicked.connect(self.start_tasks)
            self.log_utils = LogUtils('AutoTool', self.printSignal)
            self.read_config()
            self.printSignal.connect(self.print_log)
        except Exception as e:
            self.log_utils.e(traceback.format_exc())

    def save_config(self):
        self.config.host = self.host.text()
        self.config.port = self.port.text()
        self.config.task_path = self.taskPath.text()
        write_config(self.config.__dict__)

    def read_config(self):
        self.config = read_config()
        if self.config is None:
            return
        self.host.setText('' if self.config.host is None else self.config.host)
        self.port.setText('' if self.config.port is None else self.config.port)
        self.taskPath.setText('' if self.config.task_path is None else self.config.task_path)

    def start_tasks(self):
        self.save_config()
        if self.config.task_path is None or self.config.host is None or self.config.port is None:
            self.log_utils.e("Please configuration the host:port and tasks first")
            return
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
