import sys
from PyQt5 import QtWidgets
from _ruya import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
import numpy as np

class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Rüya Diyet")

        self.ui.btnHesapla.clicked.connect(self.calculateRequiredCal)

        self.ui.degisimSut.textChanged.connect(self.calculateTotalCalorie)
        self.ui.degisimEt.textChanged.connect(self.calculateTotalCalorie)
        self.ui.degisimEYG.textChanged.connect(self.calculateTotalCalorie)
        self.ui.degisimSebze.textChanged.connect(self.calculateTotalCalorie)
        self.ui.degisimYag.textChanged.connect(self.calculateTotalCalorie)
        self.ui.degisimMeyve.textChanged.connect(self.calculateTotalCalorie)
        
    def calculateRequiredCal(self):
        boy = self.ui.degerBoy.text()
        kilo = self.ui.degerKilo.text()
        yas = self.ui.degerYas.text()
        PAL = self.ui.degerPAL.text()

        try:
            if self.ui.radioButtonErkek.isChecked():
                requiredCalorieHBMale = (66.5 + (13.75 * float(kilo)) + (5.003 * float(boy)) - (6.755 * float(yas))) * float(PAL)
                self.ui.returnHarrisPAL.setText(f"Harris Benedict: {round(requiredCalorieHBMale, 2)}")

                bki = float(kilo) / ((float(boy) / 100)**2)
                self.ui.returnBKI.setText(f"BKI: {round(bki, 2)}")

                if 15<=int(yas)<=18:
                    requiredCalorieSchofieldMale = 17.6*float(kilo) + 656
                elif 19<=int(yas)<=30:
                    requiredCalorieSchofieldMale = 15.0*float(kilo) + 690
                elif 31<=int(yas)<=60:
                    requiredCalorieSchofieldMale = 11.4*float(kilo) + 870
                elif int(yas)>60:
                    requiredCalorieSchofieldMale = 11.7*float(kilo) + 585
                else:
                    requiredCalorieSchofieldMale = 0
                self.ui.returnSchofield.setText(f"Schofield: {round(requiredCalorieSchofieldMale, 2)}")

                requiredCalorieWHOMale = 24*float(kilo)
                self.ui.returnWHO.setText(f"WHO: {round(requiredCalorieWHOMale, 2)}")

            elif self.ui.radioButtonKadin.isChecked():
                requiredCalorieHBFemale = (655 + (9.563 * float(kilo)) + (1.850 * float(boy)) - (4.676 * float(yas))) * float(PAL)
                self.ui.returnHarrisPAL.setText(f"Harris Benedict: {round(requiredCalorieHBFemale, 2)}")

                bki = float(kilo) / ((float(boy) / 100)**2)
                self.ui.returnBKI.setText(f"BKI: {round(bki, 2)}")

                if 15<=int(yas)<=18:
                    requiredCalorieSchofieldFemale = 13.3*float(kilo) + 690
                elif 19<=int(yas)<=30:
                    requiredCalorieSchofieldFemale = 14.8*float(kilo) + 485
                elif 31<=int(yas)<=60:
                    requiredCalorieSchofieldFemale = 8.1*float(kilo) + 842
                elif int(yas)>60:
                    requiredCalorieSchofieldFemale = 9*float(kilo) + 856
                else:
                    requiredCalorieSchofieldFemale = 0
                self.ui.returnSchofield.setText(f"Schofield: {round(requiredCalorieSchofieldFemale, 2)}")

                requiredCalorieWHOFemale = 24*float(kilo)*0.95
                self.ui.returnWHO.setText(f"WHO: {round(requiredCalorieWHOFemale, 2)}")
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Hata")
                msg.setText("Lütfen cinsiyet seçiniz.")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("Hata")
            msg.setText("Lütfen boy, kilo, yaş ve fiziksel aktivite değerlerini sayısal olarak giriniz.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
    
    def calculateTotalCalorie(self):    
        et = self.ui.degisimEt.text()        
        sut = self.ui.degisimSut.text()        
        eyg = self.ui.degisimEYG.text()        
        sebze = self.ui.degisimSebze.text()        
        yag = self.ui.degisimYag.text()
        meyve = self.ui.degisimMeyve.text()

        try:
            total_calorie = int(et)*69 + int(sut)*114 + int(eyg)*68 + int(sebze)*28 + int(yag)*45 + int(meyve)*48
            self.ui.returnTotalCalorie.setText(str(total_calorie))

            total_CHO = 4*(int(et)*0 + int(sut)*9 + int(eyg)*15 + int(sebze)*6 + int(yag)*0 + int(meyve)*12)
            self.ui.returntotalCHO.setText(str(total_CHO))

            total_Protein = 4*(int(et)*6 + int(sut)*6 + int(eyg)*2 + int(sebze)*1 + int(yag)*0 + int(meyve)*0)
            self.ui.returntotalProtein.setText(str(total_Protein))

            total_Yag = 9*(int(et)*5 + int(sut)*6 + int(eyg)*0 + int(sebze)*0 + int(yag)*5 + int(meyve)*0)
            self.ui.returntotalYag.setText(str(total_Yag))

            self.ui.returnPercentYag.setText(str(round(total_Yag/total_calorie*100, 2)))
            self.ui.returnPercentProtein.setText(str(round(total_Protein/total_calorie*100, 2)))
            self.ui.returnPercentCHO.setText(str(round(total_CHO/total_calorie*100, 2)))

        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("Hata")
            msg.setText("Sadece rakam giriniz.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())

app()