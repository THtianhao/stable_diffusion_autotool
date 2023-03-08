import os.path
import time
from PyQt5.QtCore import QDateTime
import datetime
import logging.handlers


class LogUtils:

    def __init__(self, tag, printer):
        self.printer = printer
        self.logger = logging.getLogger("%s_log" % tag)
        self.fileTag = tag
        self.time = datetime.time(7, 0, 0)
        self.setLogger()

    def setLogger(self):
        self.logger.setLevel(logging.DEBUG)
        # path = r'%s\riotlog\%s' % (get_desktop(), self.fileTag)
        path = r'.\res\log\%s' % self.fileTag
        if not os.path.exists(path):
            os.makedirs(path)
        logFileName = r'%s\%s_log.log' % (path, self.fileTag)
        handler = logging.handlers.TimedRotatingFileHandler(logFileName, when='D', interval=1, encoding='utf-8', backupCount=7)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def i(self, log: str):
        self.logger.info(log)
        log = "%s<font size=3 color=black> %s </font>" % (QDateTime.currentDateTime().toString("[hh:mm:ss]"), log)
        self.printer.print_log(log)

    def w(self, log: str):
        self.logger.warning(log)
        log = "%s<font color=orange> %s </font>" % (QDateTime.currentDateTime().toString("[hh:mm:ss]"), log)
        self.printer.print_log(log)

    def e(self, log: str):
        self.logger.error(log)
        log = "%s<font color=red> %s </font>" % (QDateTime.currentDateTime().toString("[hh:mm:ss]"), log)
        self.printer.print_log(log)

    def sys(self, log: str):
        self.logger.info(log)
        log = "%s<font color=DarkBlue> %s </font>" % (QDateTime.currentDateTime().toString("[hh:mm:ss]"), log)
        self.printer.print_log(log)

    def separator(self):
        self.i("------------------------------------------")

    def delay(self, delayTime):
        if delayTime <= 0:
            return
        message = ""
        if type(delayTime) is float:
            message = "等待%.1f秒" % delayTime
        elif type(delayTime) is int:
            message = "等待%d秒" % delayTime
        self.i(message)
        time.sleep(delayTime)