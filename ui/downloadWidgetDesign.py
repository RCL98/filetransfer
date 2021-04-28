# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'downloadWidgetDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import icons.icons


class Ui_DownloadWidget(object):
    def setupUi(self, DownloadWidget):
        DownloadWidget.setObjectName("DownloadWidget")
        DownloadWidget.resize(944, 720)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DownloadWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.usersFrame = QtWidgets.QFrame(DownloadWidget)
        self.usersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.usersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usersFrame.setObjectName("usersFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.usersFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.browseUsersFrame = QtWidgets.QFrame(self.usersFrame)
        self.browseUsersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.browseUsersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.browseUsersFrame.setObjectName("browseUsersFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.browseUsersFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.browseUsersLabel = QtWidgets.QLabel(self.browseUsersFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.browseUsersLabel.setFont(font)
        self.browseUsersLabel.setObjectName("browseUsersLabel")
        self.horizontalLayout_2.addWidget(self.browseUsersLabel)
        self.browseUsersLineEdit = QtWidgets.QLineEdit(self.browseUsersFrame)
        self.browseUsersLineEdit.setObjectName("browseUsersLineEdit")
        self.horizontalLayout_2.addWidget(self.browseUsersLineEdit)
        self.verticalLayout_3.addWidget(self.browseUsersFrame)
        self.usersList = QtWidgets.QListWidget(self.usersFrame)
        self.usersList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.usersList.setObjectName("usersList")
        self.verticalLayout_3.addWidget(self.usersList)
        self.horizontalLayout.addWidget(self.usersFrame)
        self.buttonsFrame = QtWidgets.QFrame(DownloadWidget)
        self.buttonsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonsFrame.setObjectName("buttonsFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.buttonsFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.downloadButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.downloadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downloadButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/buttonIcons/downloadIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon)
        self.downloadButton.setIconSize(QtCore.QSize(15, 15))
        self.downloadButton.setObjectName("downloadButton")
        self.verticalLayout_4.addWidget(self.downloadButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.buttonsFrame)
        self.treeFrame = QtWidgets.QFrame(DownloadWidget)
        self.treeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.treeFrame.setObjectName("treeFrame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.treeFrame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.browseFileFrame = QtWidgets.QFrame(self.treeFrame)
        self.browseFileFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.browseFileFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.browseFileFrame.setObjectName("browseFileFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.browseFileFrame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.browseFileLabel = QtWidgets.QLabel(self.browseFileFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.browseFileLabel.setFont(font)
        self.browseFileLabel.setObjectName("browseFileLabel")
        self.horizontalLayout_4.addWidget(self.browseFileLabel)
        self.browseFileLineEdit = QtWidgets.QLineEdit(self.browseFileFrame)
        self.browseFileLineEdit.setObjectName("browseFileLineEdit")
        self.horizontalLayout_4.addWidget(self.browseFileLineEdit)
        self.verticalLayout_5.addWidget(self.browseFileFrame)
        self.fileTreeView = QtWidgets.QTreeView(self.treeFrame)
        self.fileTreeView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.fileTreeView.setObjectName("fileTreeView")
        self.verticalLayout_5.addWidget(self.fileTreeView)
        self.horizontalLayout.addWidget(self.treeFrame)
        self.browseUsersLabel.setBuddy(self.browseUsersLineEdit)
        self.browseFileLabel.setBuddy(self.browseFileLineEdit)

        self.retranslateUi(DownloadWidget)
        QtCore.QMetaObject.connectSlotsByName(DownloadWidget)

    def retranslateUi(self, DownloadWidget):
        _translate = QtCore.QCoreApplication.translate
        DownloadWidget.setWindowTitle(_translate("DownloadWidget", "Form"))
        self.browseUsersLabel.setText(_translate("DownloadWidget", "Browse Users:"))
        self.downloadButton.setText(_translate("DownloadWidget", "DownLoad"))
        self.browseFileLabel.setText(_translate("DownloadWidget", "Browse Files:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DownloadWidget = QtWidgets.QWidget()
    ui = Ui_DownloadWidget()
    ui.setupUi(DownloadWidget)
    DownloadWidget.show()
    sys.exit(app.exec_())
