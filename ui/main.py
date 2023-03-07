# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(791, 637)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(791, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.saveConfig = QtWidgets.QPushButton(self.centralwidget)
        self.saveConfig.setObjectName("saveConfig")
        self.horizontalLayout_4.addWidget(self.saveConfig)
        self.startTask = QtWidgets.QPushButton(self.centralwidget)
        self.startTask.setObjectName("startTask")
        self.horizontalLayout_4.addWidget(self.startTask)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.host = QtWidgets.QLineEdit(self.centralwidget)
        self.host.setObjectName("host")
        self.horizontalLayout.addWidget(self.host)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.port = QtWidgets.QLineEdit(self.centralwidget)
        self.port.setObjectName("port")
        self.horizontalLayout_3.addWidget(self.port)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fileConfig = QtWidgets.QLabel(self.centralwidget)
        self.fileConfig.setObjectName("fileConfig")
        self.horizontalLayout_2.addWidget(self.fileConfig)
        self.taskPath = QtWidgets.QLineEdit(self.centralwidget)
        self.taskPath.setObjectName("taskPath")
        self.horizontalLayout_2.addWidget(self.taskPath)
        self.openTaskPath = QtWidgets.QToolButton(self.centralwidget)
        self.openTaskPath.setObjectName("openTaskPath")
        self.horizontalLayout_2.addWidget(self.openTaskPath)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 40)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.logPanel = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.logPanel.setObjectName("logPanel")
        self.verticalLayout.addWidget(self.logPanel)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 791, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stable diffusion webui auto tool"))
        self.saveConfig.setText(_translate("MainWindow", "保存配置"))
        self.startTask.setText(_translate("MainWindow", "开始任务"))
        self.label.setText(_translate("MainWindow", "服务器IP"))
        self.label_3.setText(_translate("MainWindow", "端口号"))
        self.fileConfig.setText(_translate("MainWindow", "配置文件路径"))
        self.openTaskPath.setText(_translate("MainWindow", "浏览"))
        self.label_2.setText(_translate("MainWindow", "Log"))
