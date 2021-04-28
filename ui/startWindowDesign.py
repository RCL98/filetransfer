# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startWindowDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import icons.icons

class Ui_StartWindow(object):
    def setupUi(self, StartWindow):
        StartWindow.setObjectName("StartWindow")
        StartWindow.resize(1127, 688)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/windowIcons/appIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(StartWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mainFrame = QtWidgets.QFrame(self.centralwidget)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.mainGridLayout = QtWidgets.QGridLayout(self.mainFrame)
        self.mainGridLayout.setObjectName("mainGridLayout")
        self.leftFrame = QtWidgets.QFrame(self.mainFrame)
        self.leftFrame.setObjectName("leftFrame")
        self.leftVerticalLayout = QtWidgets.QVBoxLayout(self.leftFrame)
        self.leftVerticalLayout.setObjectName("leftVerticalLayout")
        self.noteFrame = QtWidgets.QFrame(self.leftFrame)
        self.noteFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.noteFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.noteFrame.setObjectName("noteFrame")
        self.noteVerticalLayout = QtWidgets.QVBoxLayout(self.noteFrame)
        self.noteVerticalLayout.setObjectName("noteVerticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.noteVerticalLayout.addItem(spacerItem)
        self.totalSizeLabel = QtWidgets.QLabel(self.noteFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.totalSizeLabel.setFont(font)
        self.totalSizeLabel.setObjectName("totalSizeLabel")
        self.noteVerticalLayout.addWidget(self.totalSizeLabel)
        self.totalFilesLabel = QtWidgets.QLabel(self.noteFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.totalFilesLabel.setFont(font)
        self.totalFilesLabel.setObjectName("totalFilesLabel")
        self.noteVerticalLayout.addWidget(self.totalFilesLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.noteVerticalLayout.addItem(spacerItem1)
        self.noteLabel = QtWidgets.QLabel(self.noteFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.noteLabel.setFont(font)
        self.noteLabel.setScaledContents(True)
        self.noteLabel.setWordWrap(True)
        self.noteLabel.setObjectName("noteLabel")
        self.noteVerticalLayout.addWidget(self.noteLabel)
        self.leftVerticalLayout.addWidget(self.noteFrame)
        self.downFrame = QtWidgets.QFrame(self.leftFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downFrame.sizePolicy().hasHeightForWidth())
        self.downFrame.setSizePolicy(sizePolicy)
        self.downFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.downFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.downFrame.setObjectName("downFrame")
        self.downVerticalLayout = QtWidgets.QVBoxLayout(self.downFrame)
        self.downVerticalLayout.setObjectName("downVerticalLayout")
        self.nameTextLabel = QtWidgets.QLabel(self.downFrame)
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
        self.downVerticalLayout.addWidget(self.nameTextLabel)
        self.acceptFrame = QtWidgets.QFrame(self.downFrame)
        self.acceptFrame.setObjectName("acceptFrame")
        self.acceptVerticalLayout = QtWidgets.QVBoxLayout(self.acceptFrame)
        self.acceptVerticalLayout.setObjectName("acceptVerticalLayout")
        self.nameFrame = QtWidgets.QFrame(self.acceptFrame)
        self.nameFrame.setObjectName("nameFrame")
        self.nameHorizontalLayout = QtWidgets.QHBoxLayout(self.nameFrame)
        self.nameHorizontalLayout.setObjectName("nameHorizontalLayout")
        self.nameLabel = QtWidgets.QLabel(self.nameFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.nameHorizontalLayout.addWidget(self.nameLabel)
        self.nameEdit = QtWidgets.QLineEdit(self.nameFrame)
        self.nameEdit.setObjectName("nameEdit")
        self.nameHorizontalLayout.addWidget(self.nameEdit)
        self.acceptVerticalLayout.addWidget(self.nameFrame)
        self.acceptButton = QtWidgets.QPushButton(self.acceptFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.acceptButton.setFont(font)
        self.acceptButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.acceptButton.setObjectName("acceptButton")
        self.acceptVerticalLayout.addWidget(self.acceptButton)
        self.downVerticalLayout.addWidget(self.acceptFrame)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.downVerticalLayout.addItem(spacerItem2)
        self.leftVerticalLayout.addWidget(self.downFrame)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.leftVerticalLayout.addItem(spacerItem3)
        self.mainGridLayout.addWidget(self.leftFrame, 0, 0, 1, 1)
        self.rightFame = QtWidgets.QFrame(self.mainFrame)
        self.rightFame.setObjectName("rightFame")
        self.rightVerticalLayout = QtWidgets.QVBoxLayout(self.rightFame)
        self.rightVerticalLayout.setSpacing(0)
        self.rightVerticalLayout.setObjectName("rightVerticalLayout")
        self.buttonsFrame = QtWidgets.QFrame(self.rightFame)
        self.buttonsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonsFrame.setObjectName("buttonsFrame")
        self.buttonsHorizontalLayout = QtWidgets.QHBoxLayout(self.buttonsFrame)
        self.buttonsHorizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.buttonsHorizontalLayout.setSpacing(3)
        self.buttonsHorizontalLayout.setObjectName("buttonsHorizontalLayout")
        self.openButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.openButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.openButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/buttonIcons/openIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openButton.setIcon(icon1)
        self.openButton.setIconSize(QtCore.QSize(48, 25))
        self.openButton.setObjectName("openButton")
        self.buttonsHorizontalLayout.addWidget(self.openButton)
        self.saveButton = QtWidgets.QPushButton(self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/buttonIcons/saveAsIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon2)
        self.saveButton.setIconSize(QtCore.QSize(48, 25))
        self.saveButton.setObjectName("saveButton")
        self.buttonsHorizontalLayout.addWidget(self.saveButton)
        self.saveAsButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.saveAsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveAsButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/buttonIcons/saveIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveAsButton.setIcon(icon3)
        self.saveAsButton.setIconSize(QtCore.QSize(48, 25))
        self.saveAsButton.setObjectName("saveAsButton")
        self.buttonsHorizontalLayout.addWidget(self.saveAsButton)
        self.undoButton = QtWidgets.QPushButton(self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.undoButton.sizePolicy().hasHeightForWidth())
        self.undoButton.setSizePolicy(sizePolicy)
        self.undoButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.undoButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/buttonIcons/undoIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undoButton.setIcon(icon4)
        self.undoButton.setIconSize(QtCore.QSize(48, 25))
        self.undoButton.setObjectName("undoButton")
        self.buttonsHorizontalLayout.addWidget(self.undoButton)
        self.redoButton = QtWidgets.QPushButton(self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redoButton.sizePolicy().hasHeightForWidth())
        self.redoButton.setSizePolicy(sizePolicy)
        self.redoButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.redoButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/buttonIcons/redoIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redoButton.setIcon(icon5)
        self.redoButton.setIconSize(QtCore.QSize(48, 25))
        self.redoButton.setObjectName("redoButton")
        self.buttonsHorizontalLayout.addWidget(self.redoButton)
        self.addButton = QtWidgets.QPushButton(self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/buttonIcons/addIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon6)
        self.addButton.setIconSize(QtCore.QSize(48, 25))
        self.addButton.setObjectName("addButton")
        self.buttonsHorizontalLayout.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QPushButton(self.buttonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        self.deleteButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/buttonIcons/deleteIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon7)
        self.deleteButton.setIconSize(QtCore.QSize(48, 25))
        self.deleteButton.setCheckable(False)
        self.deleteButton.setObjectName("deleteButton")
        self.buttonsHorizontalLayout.addWidget(self.deleteButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonsHorizontalLayout.addItem(spacerItem4)
        self.selectedSizeLabel = QtWidgets.QLabel(self.buttonsFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.selectedSizeLabel.setFont(font)
        self.selectedSizeLabel.setObjectName("selectedSizeLabel")
        self.buttonsHorizontalLayout.addWidget(self.selectedSizeLabel)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonsHorizontalLayout.addItem(spacerItem5)
        self.selectedFilesLabel = QtWidgets.QLabel(self.buttonsFrame)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.selectedFilesLabel.setFont(font)
        self.selectedFilesLabel.setObjectName("selectedFilesLabel")
        self.buttonsHorizontalLayout.addWidget(self.selectedFilesLabel)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonsHorizontalLayout.addItem(spacerItem6)
        self.rightVerticalLayout.addWidget(self.buttonsFrame)
        self.treeFrame = QtWidgets.QFrame(self.rightFame)
        self.treeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.treeFrame.setObjectName("treeFrame")
        self.treeGridLayout = QtWidgets.QGridLayout(self.treeFrame)
        self.treeGridLayout.setContentsMargins(-1, 0, -1, -1)
        self.treeGridLayout.setObjectName("treeGridLayout")
        self.treeView = QtWidgets.QTreeView(self.treeFrame)
        self.treeView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.treeView.setObjectName("treeView")
        self.treeGridLayout.addWidget(self.treeView, 0, 0, 1, 1)
        self.rightVerticalLayout.addWidget(self.treeFrame)
        self.mainGridLayout.addWidget(self.rightFame, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.mainFrame, 0, 0, 1, 1)
        StartWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(StartWindow)
        self.statusbar.setObjectName("statusbar")
        StartWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartWindow)
        QtCore.QMetaObject.connectSlotsByName(StartWindow)

    def retranslateUi(self, StartWindow):
        _translate = QtCore.QCoreApplication.translate
        StartWindow.setWindowTitle(_translate("StartWindow", "FileTransfer"))
        self.totalSizeLabel.setText(_translate("StartWindow", "Total Size: 0 GB"))
        self.totalFilesLabel.setText(_translate("StartWindow", "Total Files: 0"))
        self.noteLabel.setText(_translate("StartWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; text-decoration: underline;\">Note</span><span style=\" font-size:10pt;\">: You are not required to submit files for distribution in order to use the aplication.</span></p></body></html>"))
        self.nameTextLabel.setText(_translate("StartWindow", "<html><head/><body><p align=\"center\">This is the name that will appear to the other users. By default the chosen name is the name of the machine.</p></body></html>"))
        self.nameLabel.setText(_translate("StartWindow", "Name:"))
        self.acceptButton.setText(_translate("StartWindow", "Accept"))
        self.selectedSizeLabel.setText(_translate("StartWindow", "Selected Size: 0 GB"))
        self.selectedFilesLabel.setText(_translate("StartWindow", "Selected Files: 0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StartWindow = QtWidgets.QMainWindow()
    ui = Ui_StartWindow()
    ui.setupUi(StartWindow)
    StartWindow.show()
    sys.exit(app.exec_())
