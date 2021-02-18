# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startUpdated.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from psutil import disk_partitions
from socket import gethostname
import mainWindow


class Ui_StartWindow(object):
    def __init__(self, window):
        self.window = window
        self.centralWidget = QtWidgets.QWidget(window)
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.mainFrame = QtWidgets.QFrame(self.centralWidget)
        self.gridLayout_5 = QtWidgets.QGridLayout(self.mainFrame)
        self.treeFileFrame = QtWidgets.QFrame(self.mainFrame)
        self.treeView = QtWidgets.QTreeView(self.treeFileFrame)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.treeFileFrame)
        self.treeFileLabel = QtWidgets.QLabel(self.treeFileFrame)
        self.buttonsFrame = QtWidgets.QFrame(self.mainFrame)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.buttonsFrame)
        self.upFrame = QtWidgets.QFrame(self.buttonsFrame)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.upFrame)
        self.line_0 = QtWidgets.QFrame(self.upFrame)
        self.comboLabel = QtWidgets.QLabel(self.upFrame)
        self.combFrame = QtWidgets.QFrame(self.upFrame)
        self.gridLayout_6 = QtWidgets.QGridLayout(self.combFrame)
        self.comboBox = QtWidgets.QComboBox(self.combFrame)
        self.noteLabel = QtWidgets.QLabel(self.upFrame)
        self.downFrame = QtWidgets.QFrame(self.buttonsFrame)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.downFrame)
        self.line_1 = QtWidgets.QFrame(self.downFrame)
        self.nameTextLabel = QtWidgets.QLabel(self.downFrame)
        self.line_2 = QtWidgets.QFrame(self.downFrame)
        self.acceptFrame = QtWidgets.QFrame(self.downFrame)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.acceptFrame)
        self.nameFrame = QtWidgets.QFrame(self.acceptFrame)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.nameFrame)
        self.nameLabel = QtWidgets.QLabel(self.nameFrame)
        self.nameEdit = QtWidgets.QLineEdit(self.nameFrame)
        self.acceptNameBtn = QtWidgets.QPushButton(self.acceptFrame)
        self.statusBar = QtWidgets.QStatusBar(window)
        self.setupUi()

    def acceptClick(self):
        self.mainWin = QtWidgets.QMainWindow()
        self.ui = mainWindow.Ui_MainWindow(self.mainWin)
        self.window.close()
        self.mainWin.show()

    def setupUi(self):
        self.window.setObjectName("StartWindow")
        self.window.resize(800, 600)
        self.centralWidget.setObjectName("centralwidget")
        self.gridLayout.setObjectName("gridLayout")
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.treeFileFrame.setObjectName("treeFileFrame")
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.treeFileLabel.setObjectName("treeFileLabel")
        self.verticalLayout_4.addWidget(self.treeFileLabel)
        self.treeView.setObjectName("treeView")
        self.verticalLayout_4.addWidget(self.treeView)
        self.gridLayout_5.addWidget(self.treeView, 0, 1, 1, 1)

        self.buttonsFrame.setObjectName("buttonsFrame")
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.upFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.upFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.upFrame.setObjectName("upFrame")
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.line_0.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_0.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_0.setObjectName("line_0")
        self.verticalLayout_3.addWidget(self.line_0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboLabel.sizePolicy().hasHeightForWidth())
        self.comboLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.comboLabel.setFont(font)
        self.comboLabel.setScaledContents(True)
        self.comboLabel.setWordWrap(True)
        self.comboLabel.setObjectName("comboLabel")
        self.verticalLayout_3.addWidget(self.comboLabel)
        self.combFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.combFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.combFrame.setObjectName("combFrame")
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.comboBox.setObjectName("comboBox")

        for part in disk_partitions():
            self.comboBox.addItem(part.mountpoint)

        self.gridLayout_6.addWidget(self.comboBox, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.combFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.noteLabel.setFont(font)
        self.noteLabel.setScaledContents(True)
        self.noteLabel.setWordWrap(True)
        self.noteLabel.setObjectName("noteLabel")
        self.verticalLayout_3.addWidget(self.noteLabel)
        self.verticalLayout_2.addWidget(self.upFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downFrame.sizePolicy().hasHeightForWidth())
        self.downFrame.setSizePolicy(sizePolicy)
        self.downFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.downFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.downFrame.setObjectName("downFrame")
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.gridLayout_2.addWidget(self.line_1, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameTextLabel.sizePolicy().hasHeightForWidth())
        self.nameTextLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.nameTextLabel.setFont(font)
        self.nameTextLabel.setScaledContents(True)
        self.nameTextLabel.setWordWrap(True)
        self.nameTextLabel.setObjectName("nameTextLabel")
        self.gridLayout_2.addWidget(self.nameTextLabel, 1, 0, 1, 1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 4, 0, 1, 1)
        self.acceptFrame.setObjectName("acceptFrame")
        self.verticalLayout.setObjectName("verticalLayout")
        self.nameFrame.setObjectName("nameFrame")
        self.horizontalLayout.setObjectName("horizontalLayout")
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.horizontalLayout.addWidget(self.nameLabel)
        self.nameEdit.setObjectName("nameEdit")
        self.nameEdit.setPlaceholderText(gethostname())
        self.horizontalLayout.addWidget(self.nameEdit)
        self.verticalLayout.addWidget(self.nameFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.acceptNameBtn.setFont(font)
        self.acceptNameBtn.setObjectName("acceptNameBtn")
        self.verticalLayout.addWidget(self.acceptNameBtn)
        self.gridLayout_2.addWidget(self.acceptFrame, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.downFrame)
        self.gridLayout_5.addWidget(self.buttonsFrame, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.mainFrame, 0, 0, 1, 1)
        self.window.setCentralWidget(self.centralWidget)
        self.statusBar.setObjectName("statusbar")
        self.window.setStatusBar(self.statusBar)

        self.retranslateUi()
        self.acceptNameBtn.clicked.connect(self.acceptClick)
        QtCore.QMetaObject.connectSlotsByName(StartWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.window.setWindowTitle(_translate("StartWindow", "FileTransfer"))
        self.comboLabel.setText(_translate("StartWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Choose the partition from which you want to distribute files:</span></p></body></html>"))
        self.noteLabel.setText(_translate("StartWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; text-decoration: underline;\">Note</span><span style=\" font-size:10pt;\">: You are not required to submit files for distribution in order to use the aplication.</span></p></body></html>"))
        self.nameTextLabel.setText(_translate("StartWindow", "<html><head/><body><p align=\"center\">This is the name that will appear to the other users. By default the chosen name is the name of the machine.</p></body></html>"))
        self.nameLabel.setText(_translate("StartWindow", "Name:"))
        self.acceptNameBtn.setText(_translate("StartWindow", "Accept"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StartWindow = QtWidgets.QMainWindow()
    ui = Ui_StartWindow(StartWindow)
    StartWindow.show()
    sys.exit(app.exec_())
