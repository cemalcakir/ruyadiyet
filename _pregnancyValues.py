# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_pregnancyValues.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(804, 919)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.clientTCKN = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.clientTCKN.setFont(font)
        self.clientTCKN.setFrameShape(QtWidgets.QFrame.Box)
        self.clientTCKN.setText("")
        self.clientTCKN.setObjectName("clientTCKN")
        self.gridLayout.addWidget(self.clientTCKN, 0, 0, 1, 2)
        self.clientName = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.clientName.setFont(font)
        self.clientName.setFrameShape(QtWidgets.QFrame.Box)
        self.clientName.setText("")
        self.clientName.setObjectName("clientName")
        self.gridLayout.addWidget(self.clientName, 0, 2, 1, 2)
        self.btnKayitListele = QtWidgets.QPushButton(Form)
        self.btnKayitListele.setObjectName("btnKayitListele")
        self.gridLayout.addWidget(self.btnKayitListele, 1, 0, 1, 1)
        self.btnKayitEkle = QtWidgets.QPushButton(Form)
        self.btnKayitEkle.setObjectName("btnKayitEkle")
        self.gridLayout.addWidget(self.btnKayitEkle, 1, 1, 1, 1)
        self.btnKaydiGuncelle = QtWidgets.QPushButton(Form)
        self.btnKaydiGuncelle.setObjectName("btnKaydiGuncelle")
        self.gridLayout.addWidget(self.btnKaydiGuncelle, 1, 2, 1, 1)
        self.btnKaydiSil = QtWidgets.QPushButton(Form)
        self.btnKaydiSil.setObjectName("btnKaydiSil")
        self.gridLayout.addWidget(self.btnKaydiSil, 1, 3, 1, 1)
        self.btnCikis = QtWidgets.QPushButton(Form)
        self.btnCikis.setObjectName("btnCikis")
        self.gridLayout.addWidget(self.btnCikis, 1, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 2)
        self.tblClientValues = QtWidgets.QTableWidget(Form)
        self.tblClientValues.setRowCount(29)
        self.tblClientValues.setColumnCount(50)
        self.tblClientValues.setObjectName("tblClientValues")
        self.gridLayout.addWidget(self.tblClientValues, 3, 0, 1, 5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnKayitListele.setText(_translate("Form", "Kayıtları Listele"))
        self.btnKayitEkle.setText(_translate("Form", "Kayıt Ekle"))
        self.btnKaydiGuncelle.setText(_translate("Form", "Kaydı Güncelle"))
        self.btnKaydiSil.setText(_translate("Form", "Kaydı Sil"))
        self.btnCikis.setText(_translate("Form", "Çıkış"))
        self.label_4.setText(_translate("Form", "DANIŞAN KAYITLARI"))
