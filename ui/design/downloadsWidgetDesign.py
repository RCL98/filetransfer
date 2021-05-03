# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'downloadsWidgetDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_downloadsForm(object):
    def setupUi(self, downloadsForm):
        downloadsForm.setObjectName("downloadsForm")
        downloadsForm.resize(907, 610)
        self.gridLayout_3 = QtWidgets.QGridLayout(downloadsForm)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.downTableFrame = QtWidgets.QFrame(downloadsForm)
        self.downTableFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.downTableFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.downTableFrame.setObjectName("downTableFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.downTableFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.downsTable = QtWidgets.QTableWidget(self.downTableFrame)
        self.downsTable.setObjectName("downsTable")
        self.downsTable.setColumnCount(4)
        self.downsTable.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsTable.setItem(0, 3, item)
        self.gridLayout.addWidget(self.downsTable, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.downTableFrame, 0, 0, 1, 1)
        self.detailsFrame = QtWidgets.QFrame(downloadsForm)
        self.detailsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.detailsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.detailsFrame.setObjectName("detailsFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.detailsFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.detailsFrame)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/windowIcons/fileIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.generalTab, icon, "")
        self.contenTab = QtWidgets.QWidget()
        self.contenTab.setObjectName("contenTab")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/buttonIcons/openIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.contenTab, icon1, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.detailsFrame, 1, 0, 1, 1)

        self.retranslateUi(downloadsForm)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(downloadsForm)

    def retranslateUi(self, downloadsForm):
        _translate = QtCore.QCoreApplication.translate
        downloadsForm.setWindowTitle(_translate("downloadsForm", "Form"))
        item = self.downsTable.verticalHeaderItem(0)
        item.setText(_translate("downloadsForm", "1"))
        item = self.downsTable.verticalHeaderItem(1)
        item.setText(_translate("downloadsForm", "2"))
        item = self.downsTable.horizontalHeaderItem(0)
        item.setText(_translate("downloadsForm", "Name"))
        item = self.downsTable.horizontalHeaderItem(1)
        item.setText(_translate("downloadsForm", "Dimension"))
        item = self.downsTable.horizontalHeaderItem(2)
        item.setText(_translate("downloadsForm", "Progress"))
        item = self.downsTable.horizontalHeaderItem(3)
        item.setText(_translate("downloadsForm", "Down speed"))
        __sortingEnabled = self.downsTable.isSortingEnabled()
        self.downsTable.setSortingEnabled(False)
        item = self.downsTable.item(0, 0)
        item.setText(_translate("downloadsForm", "User1"))
        item = self.downsTable.item(0, 1)
        item.setText(_translate("downloadsForm", "54,6 GB"))
        item = self.downsTable.item(0, 2)
        item.setText(_translate("downloadsForm", "76%"))
        item = self.downsTable.item(0, 3)
        item.setText(_translate("downloadsForm", "34 Mb/s"))
        self.downsTable.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("downloadsForm", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.contenTab), _translate("downloadsForm", "Content"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    downloadsForm = QtWidgets.QWidget()
    ui = Ui_downloadsForm()
    ui.setupUi(downloadsForm)
    downloadsForm.show()
    sys.exit(app.exec_())