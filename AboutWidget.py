# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutWidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AboutWidget(object):
    def setupUi(self, AboutWidget):
        AboutWidget.setObjectName(_fromUtf8("AboutWidget"))
        AboutWidget.resize(400, 300)
        self.AboutLabel = QtGui.QLabel(AboutWidget)
        self.AboutLabel.setGeometry(QtCore.QRect(100, 10, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.AboutLabel.setFont(font)
        self.AboutLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.AboutLabel.setTextFormat(QtCore.Qt.AutoText)
        self.AboutLabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.AboutLabel.setObjectName(_fromUtf8("AboutLabel"))
        self.label = QtGui.QLabel(AboutWidget)
        self.label.setGeometry(QtCore.QRect(20, 50, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(AboutWidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(AboutWidget)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 361, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(AboutWidget)
        QtCore.QMetaObject.connectSlotsByName(AboutWidget)

    def retranslateUi(self, AboutWidget):
        AboutWidget.setWindowTitle(_translate("AboutWidget", "About", None))
        self.AboutLabel.setText(_translate("AboutWidget", "About", None))
        self.label.setText(_translate("AboutWidget", "Version:  1.0", None))
        self.label_2.setText(_translate("AboutWidget", "Author:  Travis Hoy (travis.hoy1@gmail.com)", None))
        self.label_3.setText(_translate("AboutWidget", "Disclaimer: This program is not affiliated with Brigham Young University in any way. It was created by a student of the university for the simple use of checking one\'s grades and is not intended for any other purpose. Usernames and passwords provided by users do not come with any guarantees or assurances of security. The author of the program is not responsible for its misuse.", None))

