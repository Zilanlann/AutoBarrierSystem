# Form implementation generated from reading ui file 'passdialog.ui'
#
# Created by: PyQt6 UI code generator 6.5.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PassDialog(object):
    def setupUi(self, PassDialog):
        PassDialog.setObjectName("PassDialog")
        PassDialog.resize(452, 363)
        PassDialog.setMinimumSize(QtCore.QSize(452, 363))
        PassDialog.setMaximumSize(QtCore.QSize(452, 363))
        self.layoutWidget = QtWidgets.QWidget(parent=PassDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 230, 221, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.CancelPushButton = PushButton(parent=self.layoutWidget)
        self.CancelPushButton.setObjectName("CancelPushButton")
        self.horizontalLayout_4.addWidget(self.CancelPushButton)
        self.ConfirmPushButton = PrimaryPushButton(parent=self.layoutWidget)
        self.ConfirmPushButton.setObjectName("ConfirmPushButton")
        self.horizontalLayout_4.addWidget(self.ConfirmPushButton)
        self.layoutWidget_2 = QtWidgets.QWidget(parent=PassDialog)
        self.layoutWidget_2.setGeometry(QtCore.QRect(110, 60, 251, 171))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BodyLabel = BodyLabel(parent=self.layoutWidget_2)
        self.BodyLabel.setObjectName("BodyLabel")
        self.horizontalLayout.addWidget(self.BodyLabel, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.username = LineEdit(parent=self.layoutWidget_2)
        self.username.setObjectName("username")
        self.horizontalLayout.addWidget(self.username)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.BodyLabel_2 = BodyLabel(parent=self.layoutWidget_2)
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.horizontalLayout_2.addWidget(self.BodyLabel_2)
        self.oldpassword = PasswordLineEdit(parent=self.layoutWidget_2)
        self.oldpassword.setObjectName("oldpassword")
        self.horizontalLayout_2.addWidget(self.oldpassword)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.BodyLabel_3 = BodyLabel(parent=self.layoutWidget_2)
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.horizontalLayout_3.addWidget(self.BodyLabel_3, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.newpassword = PasswordLineEdit(parent=self.layoutWidget_2)
        self.newpassword.setObjectName("newpassword")
        self.horizontalLayout_3.addWidget(self.newpassword)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(PassDialog)
        QtCore.QMetaObject.connectSlotsByName(PassDialog)

    def retranslateUi(self, PassDialog):
        _translate = QtCore.QCoreApplication.translate
        PassDialog.setWindowTitle(_translate("PassDialog", "修改密码"))
        self.CancelPushButton.setText(_translate("PassDialog", "取消"))
        self.ConfirmPushButton.setText(_translate("PassDialog", "确认"))
        self.BodyLabel.setText(_translate("PassDialog", "用户名"))
        self.BodyLabel_2.setText(_translate("PassDialog", "旧密码"))
        self.BodyLabel_3.setText(_translate("PassDialog", "新密码"))
from qfluentwidgets import BodyLabel, LineEdit, PasswordLineEdit, PrimaryPushButton, PushButton