# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExportWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Export(object):
    def setupUi(self, Dialog_Export):
        Dialog_Export.setObjectName("Dialog_Export")
        Dialog_Export.resize(174, 72)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Export)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog_Export)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_Export)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_Export)
        self.buttonBox.accepted.connect(Dialog_Export.accept)
        self.buttonBox.rejected.connect(Dialog_Export.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Export)

    def retranslateUi(self, Dialog_Export):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Export.setWindowTitle(_translate("Dialog_Export", "数据导出"))