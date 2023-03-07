from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui

from bean.task_bean import TasksBean
from config import *
from ui.main import Ui_MainWindow

class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.file_tag = "chrome_config"
        self.saveConfig.clicked.connect(save_config)
        self.openTaskPath.clicked.connect(self.open_task_path)
        self.startTask.clicked.connect(self.start_tasks)
        self.read_config()

    def read_config(self):
        read_config()
        tmpHost = config.get(host_flag)
        tmpPort = config.get(port_flag)
        tmpTask = config.get(tasks_flag)
        self.host.setText('' if tmpHost is None else tmpHost)
        self.port.setText('' if tmpPort is None else tmpPort)
        self.taskPath.setText('' if tmpTask is None else tmpTask)

    def start_tasks(self):
        tasks = self.read_task()
        if tasks == '':
            return
        tasks_bean = TasksBean()
        tasks_bean.__dict__ = tasks

    def print_log(self, log):
        self.logPanel.append(log)
        self.logPanel.ensureCursorVisible()

    def read_task(self) -> str:
        if not os.path.exists(self.config.get(self.tasks_flag)):
            self.print_log("tasks file not exist")
            return ''
        try:
            with open(self.config.get(self.tasks_flag)) as f:
                return json.load(f)
        except Exception as e:
            print(e)

    def click_start(self):
        pass

    def delete_dir(self):
        pass

    def open_task_path(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件夹", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        self.taskPath.setText(fileName)
        write_config(self.tasks_flag, fileName)

