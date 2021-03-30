import pkg_resources.py2_warn
import sys
from PyQt5 import QtWidgets
from _ruya import Ui_MainWindow
from _clientDB import Ui_Form
from _clientValues import Ui_Form as Ui_ValueForm
from _pregnancyValues import Ui_Form as Ui_PregnancyForm
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
import sqlite3
import datetime
import locale
import matplotlib.pyplot
locale.setlocale(
    category=locale.LC_ALL,
    locale="Turkish")


class DiyetApp(QtWidgets.QMainWindow):
    "Programın ana ekranı."

    def __init__(self):
        super(DiyetApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle('Rüya Diyet')
        self.setGeometry(0, 0, 900, 600)
        self.statusBar().setStyleSheet('background-color : white')
        self.ClientDB = None
        self.PregnancyDB = None
        self.onlyInt()
        self.ui.btnHesapla.clicked.connect(self.calculateRequiredCal)
        self.textChanged()
        self.ui.btnDanisanKaydi.clicked.connect(self.show_ClientDB)
        self.ui.btnDanisanGebe.clicked.connect(self.show_PregnancyDB)
        self.ui.btnTemizle.clicked.connect(self.clearValues)
        self.ui.btnMainCikis.clicked.connect(self.close)

    def calculateRequiredCal(self):
        height = self.ui.valueBoy.text().replace(",", ".")
        weight = self.ui.valueKilo.text().replace(",", ".")
        age = self.ui.valueYas.text().replace(",", ".")
        PAL = self.ui.valuePAL.text().replace(",", ".")

        male = self.ui.radioButtonErkek.isChecked()
        female = self.ui.radioButtonKadin.isChecked()

        while True:
            # Eğer herhangi bir cinsiyet işaretlenmemişse işlemi durdur ve uyarı mesajı ver
            if not (male or female):
                self.genderError()
                break
            # Eğer herhangi biri null'sa işlemi durdur ve uyarı mesajı ver
            if not (bool(height) and bool(weight) and bool(age) and bool(PAL)):
                self.valueError()
                break
                # Boy 0 girildiyse işlemi durdur ve uyarı mesajı ver. 0'a bölme hatasından kurtulmak için.
            if not (float(height)):
                self.valueError()
                break

            bki = float(weight) / ((float(height) / 100)**2)
            self.ui.returnBKI.setText(f"BKI: {round(bki, 2)}")

            """Aşağıdaki sayıları değişkenlere ata demiştin ama burada şöyle bi sorun var bu sayıların bir ismi yok
            dolayısıyla verdiğim değişken isimleri de anlamsız olacaktı ve karışacaktı. Bunların hard-coded olmasında sorun yok
            gibi geldi ama yine de yapmak gerekiyorsa liste şeklinde değişkenlere atayıp degisken[1] şeklinde geri alabilirim."""
            requiredCalorieHBSwitcher = {
                male: (66.5 + (13.75 * float(weight)) + (5.003 * float(height)) - (6.755 * float(age))) * float(PAL),
                female: (655 + (9.563 * float(weight)) + (1.850 * float(height)) -
                         (4.676 * float(age))) * float(PAL)
            }
            requiredCalorieHB = requiredCalorieHBSwitcher.get(True)
            self.ui.returnHarrisPAL.setText(
                f"Harris Benedict: {round(requiredCalorieHB, 2)}")

            requiredCalorieSchofieldSwitcher = {
                male: {
                    15 <= float(age) <= 18: 17.6*float(weight) + 656,
                    19 <= float(age) <= 30: 15.0*float(weight) + 690,
                    31 <= float(age) <= 60: 11.4*float(weight) + 870,
                    float(age) > 60: 11.7*float(weight) + 585,
                    float(age) < 15: 0
                },
                female: {
                    15 <= float(age) <= 18: 13.3*float(weight) + 690,
                    19 <= float(age) <= 30: 14.8*float(weight) + 485,
                    31 <= float(age) <= 60: 8.1 * float(weight) + 842,
                    float(age) > 60: 9 * float(weight) + 856,
                    float(age) < 15: 0
                }
            }
            requiredCalorieSchofield = requiredCalorieSchofieldSwitcher.get(
                True).get(True)
            self.ui.returnSchofield.setText(
                f"Schofield: {round(requiredCalorieSchofield, 2)}")
            if requiredCalorieSchofield == 0:
                self.ui.statusbar.showMessage(
                    "15 yaş altı için Schofield formülü kullanılamıyor.", 5000)

            requiredCalorieWHOSwitcher = {
                male: 24 * float(weight),
                female:  24 * float(weight)*0.95
            }
            requiredCalorieWHO = requiredCalorieWHOSwitcher.get(True)
            self.ui.returnWHO.setText(f"WHO: {round(requiredCalorieWHO, 2)}")

            requiredCalorieMifflinSwitcher = {
                male: 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5,
                female: 10 * float(weight) + 6.25 *
                float(height) - 5 * float(age) - 161
            }
            requiredCalorieMifflin = requiredCalorieMifflinSwitcher.get(True)
            self.ui.returnMifflin.setText(
                f"Mifflin - St Jeor: {round(requiredCalorieMifflin, 2)}")
            break

    def calculateTotalCalorie(self):
        et = self.ui.valueEt.text().replace(',', '.')
        sut = self.ui.valueSut.text().replace(',', '.')
        eyg = self.ui.valueEYG.text().replace(',', '.')
        sebze = self.ui.valueSebze.text().replace(',', '.')
        yag = self.ui.valueYag.text().replace(',', '.')
        meyve = self.ui.valueMeyve.text().replace(',', '.')
        while True:
            if not (et.isdigit() and sut.isdigit() and eyg.isdigit() and sebze.isdigit() and yag.isdigit() and meyve.isdigit()):
                break
            total_calorie = int(et) * 69 + int(sut) * 114 + int(eyg) * \
                68 + int(sebze) * 28 + int(yag) * 45 + int(meyve) * 48
            self.ui.returnTotalCalorie.setText(str(total_calorie))
            total_CHO = 4 * (int(et) * 0 + int(sut) * 9 + int(eyg)
                             * 15 + int(sebze) * 6 + int(yag) * 0 + int(meyve) * 12)
            self.ui.returntotalCHO.setText(str(total_CHO))
            total_protein = 4 * (int(et) * 6 + int(sut) * 6 + int(eyg)
                                 * 2 + int(sebze) * 1 + int(yag) * 0 + int(meyve) * 0)
            self.ui.returntotalProtein.setText(str(total_protein))
            total_yag = 9 * (int(et) * 5 + int(sut) * 6 + int(eyg)
                             * 0 + int(sebze) * 0 + int(yag) * 5 + int(meyve) * 0)
            self.ui.returntotalYag.setText(str(total_yag))
            if not total_calorie:
                break
            self.ui.returnPercentYag.setText(
                str(round(total_yag / total_calorie * 100, 2)))
            self.ui.returnPercentProtein.setText(
                str(round(total_protein / total_calorie * 100, 2)))
            self.ui.returnPercentCHO.setText(
                str(round(total_CHO / total_calorie * 100, 2)))
            break

    def onlyInt(self):
        self.ui.valueBoy.setValidator(QDoubleValidator())
        self.ui.valueKilo.setValidator(QDoubleValidator())
        self.ui.valueYas.setValidator(QDoubleValidator())
        self.ui.valuePAL.setValidator(QDoubleValidator())
        self.ui.valueSut.setValidator(QIntValidator())
        self.ui.valueEt.setValidator(QIntValidator())
        self.ui.valueEYG.setValidator(QIntValidator())
        self.ui.valueSebze.setValidator(QIntValidator())
        self.ui.valueMeyve.setValidator(QIntValidator())
        self.ui.valueYag.setValidator(QIntValidator())

    def textChanged(self):
        self.ui.valueSut.textChanged.connect(self.calculateTotalCalorie)
        self.ui.valueEt.textChanged.connect(self.calculateTotalCalorie)
        self.ui.valueEYG.textChanged.connect(self.calculateTotalCalorie)
        self.ui.valueSebze.textChanged.connect(self.calculateTotalCalorie)
        self.ui.valueYag.textChanged.connect(self.calculateTotalCalorie)
        self.ui.valueMeyve.textChanged.connect(self.calculateTotalCalorie)

    def clearValues(self):
        self.ui.valueBoy.clear()
        self.ui.valueKilo.clear()
        self.ui.valueYas.clear()
        self.ui.valuePAL.clear()

    def genderError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText('Lütfen cinsiyet seçiniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def valueError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText(
            'Lütfen boy, kilo, yaş ve fiziksel aktivite değerlerini sayısal olarak giriniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def show_ClientDB(self):
        if self.ClientDB is None:
            self.ClientDB = ClientDB()
        self.ClientDB.show()
        self.ClientDB.ui.tblSaveClient.setItem(
            0, 5, QtWidgets.QTableWidgetItem(self.ui.valueBoy.text()))
        self.ClientDB.ui.tblSaveClient.setItem(
            0, 7, QtWidgets.QTableWidgetItem(self.ui.valueKilo.text()))
        self.ClientDB.ui.tblSaveClient.setItem(0, 8, QtWidgets.QTableWidgetItem(
            self.ui.returnBKI.text().replace("BKI: ", "")))

    def show_PregnancyDB(self):
        if self.PregnancyDB is None:
            self.PregnancyDB = PregnancyDB()
        self.PregnancyDB.show()
        self.PregnancyDB.ui.tblSaveClient.setItem(
            0, 5, QtWidgets.QTableWidgetItem(self.ui.valueBoy.text()))
        self.PregnancyDB.ui.tblSaveClient.setItem(
            0, 7, QtWidgets.QTableWidgetItem(self.ui.valueKilo.text()))
        self.PregnancyDB.ui.tblSaveClient.setItem(0, 8, QtWidgets.QTableWidgetItem(
            self.ui.returnBKI.text().replace("BKI: ", "")))


class ClientDB(QtWidgets.QWidget):
    "Danışan kayıtları."

    def __init__(self):
        super(ClientDB, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle('Danışan Kayıt Formu')
        self.setGeometry(250, 75, 1542, 1100)
        self.createDatabase()
        self.tableHeaders()
        self.listClients()
        self.ui.tblClientData.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)
        self.searchTrigger()
        self.ui.btnDanisanEkle.clicked.connect(self.addClient)
        self.ui.btnTemizle.clicked.connect(self.clearSearch)
        self.ui.tblClientData.cellChanged.connect(self.updateClient)
        self.ui.btnDanisanSil.clicked.connect(self.deleteEntry)
        self.ClientRecords = None
        self.ui.btnDanisanEkrani.clicked.connect(self.show_ClientRecords)
        self.ui.btnCikis.clicked.connect(self.close)

    def createDatabase(self):
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clients (tckn text primary key, name text not null, surname text not null,
                        phonenumber text, birthdate text, height text, strDate text, strWeight text, strBKI text,strWaist text,
                        strHips text, strWaistHipsRatio text)''')
        connection.commit()
        connection.close()

    def addClient(self):
        while True:
            values = []
            clientData = self.ui.tblSaveClient.item
            if not (clientData(0, 0) and clientData(0, 1) and clientData(0, 2)):
                self.userError()
                break
            for i in range(12):
                if not clientData(0, i):
                    values.append('-')
                else:
                    values.append(clientData(0, i).text())
            else:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute(
                    'INSERT OR IGNORE INTO clients (tckn, name, surname, phonenumber, birthdate, height, strDate, strWeight, strBKI, strWaist, strHips, strWaistHipsRatio) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', values)
                if not connection.total_changes:
                    self.duplicateEntryError()
                else:
                    self.inputSuccessfull()
                    self.ui.tblSaveClient.clearContents()
                connection.commit()
                connection.close()
                break
        self.listClients()

    def listClients(self):
        self.ui.tblClientData.clear()
        self.tableHeaders()
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clients')
        for rowIndex, rowData in enumerate(cursor):
            for columnIndex, columnData in enumerate(rowData):
                self.ui.tblClientData.setItem(
                    rowIndex, columnIndex, QtWidgets.QTableWidgetItem(str(columnData)))
        connection.commit()
        connection.close()

    def updateClient(self):
        selected = self.ui.tblClientData.selectedItems()
        if len(selected) == 12:
            answer = QMessageBox.question(
                self, 'Kaydı Güncelle', f"{selected[0].text()} tc kimlik numaralı {selected[1].text()} {selected[2].text()} kaydını güncellemek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE clients SET name=?, surname=?, phonenumber=?, birthdate=?, height=?, strDate=?, strWeight=?, strBKI=?, strWaist=?, strHips=?, strWaistHipsRatio=? WHERE tckn=?',
                               (selected[1].text(), selected[2].text(),
                                selected[3].text(), selected[4].text(
                               ), selected[5].text(),
                                   selected[6].text(), selected[7].text(
                               ), selected[8].text(),
                                   selected[9].text(), selected[10].text(), selected[11].text(), selected[0].text()))
                connection.commit()
                connection.close()
                self.listClients()

    def deleteEntry(self):
        selected = self.ui.tblClientData.selectedItems()
        if len(selected) == 12:
            answer = QMessageBox.question(
                self, 'Kaydı Sil', f"""{selected[0].text()} tc kimlik numaralı {selected[1].text()} {selected[2].text()} isimli kaydı silmek istiyor musunuz?""", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute("DELETE FROM clients WHERE tckn='%s'" %
                               selected[0].text())
                connection.commit()
                connection.close()
                self.listClients()

    def searchClient(self):
        searchByTckn = self.ui.lineSearchTCKN.text()
        searchByName = self.ui.lineSearchName.text()
        searchBySurname = self.ui.lineSearchSurname.text()
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * from clients WHERE tckn LIKE ? || '%' AND name LIKE ? || '%' AND surname LIKE ? || '%'", (
            searchByTckn, searchByName, searchBySurname))
        self.ui.tblClientData.clearContents()
        for rowIndex, rowData in enumerate(cursor):
            for columnIndex, columnData in enumerate(rowData):
                self.ui.tblClientData.setItem(
                    owIndex, columnIndex, QtWidgets.QTableWidgetItem(str(columnData)))
        connection.commit()
        connection.close()

    def searchTrigger(self):
        self.ui.lineSearchTCKN.textChanged.connect(self.searchClient)
        self.ui.lineSearchName.textChanged.connect(self.searchClient)
        self.ui.lineSearchSurname.textChanged.connect(self.searchClient)

    def clearSearch(self):
        self.ui.lineSearchTCKN.clear()
        self.ui.lineSearchName.clear()
        self.ui.lineSearchSurname.clear()
        self.listClients()

    def tableHeaders(self):
        self.ui.tblClientData.setHorizontalHeaderLabels(('TCKN', 'Ad', 'Soyad', 'Telefon No', 'Doğum Tarihi', 'Boy', 'Başlangıç Tarihi',
                                                         'Başlangıç Kilo', 'Başlangıç BKI', 'Başlangıç Bel', 'Başlangıç Kalça',
                                                         'Bşlgnç. Bel/Kalça'))
        self.ui.tblSaveClient.setHorizontalHeaderLabels(('TCKN', 'Ad', 'Soyad', 'Telefon No', 'Doğum Tarihi', 'Boy', 'Başlangıç Tarihi',
                                                         'Başlangıç Kilo', 'Başlangıç BKI', 'Başlangıç Bel', 'Başlangıç Kalça',
                                                         'Bşlgnç. Bel/Kalça'))
        self.ui.tblSaveClient.setVerticalHeaderLabels(('Ekle',))

    def userError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText('Kullanıcı kaydı için Tckn, Ad ve Soyad Giriniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def duplicateEntryError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText("Bu Tckn'ye ait bir kayıt zaten mevcut.")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def inputSuccessfull(self):
        msg = QMessageBox()
        msg.setWindowTitle('Kayıt Eklendi')
        msg.setText('Kaydınız başarıyla eklendi.')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def selectClientError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText(
            'Listeden bilgilerini görüntülemek istediğiniz danışanı seçiniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def show_ClientRecords(self):
        if self.ClientRecords is None:
            self.ClientRecords = ClientRecords()
        if self.ui.tblClientData.selectedItems():
            tckn = self.ui.tblClientData.selectedItems()[0].text()
            self.ClientRecords.show()
            self.ClientRecords.ui.clientTCKN.setText(
                self.ui.tblClientData.selectedItems()[0].text())
            self.ClientRecords.ui.clientName.setText(self.ui.tblClientData.selectedItems()[
                                                     1].text() + " " + self.ui.tblClientData.selectedItems()[2].text())
        else:
            self.selectClientError()


class PregnancyDB(ClientDB):
    "Gebe Danışan Kayıtları."

    def __init__(self):
        super(PregnancyDB, self).__init__()
        self.setWindowTitle('Gebe Kayıt Formu')
        self.PregnancyRecords = None
        self.ui.btnDanisanEkrani.clicked.connect(self.show_ClientRecords)

    def createDatabase(self):
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS p_clients (tckn text primary key, name text not null, surname text not null,
                        phonenumber text, birthdate text, height text, strDate text, strWeight text, strBKI text,strWaist text,
                        strHips text, strWaistHipsRatio text)''')
        connection.commit()
        connection.close()

    def addClient(self):
        while True:
            values = []
            clientData = self.ui.tblSaveClient.item
            if not (clientData(0, 0) and clientData(0, 1) and clientData(0, 2)):
                self.userError()
                break
            for i in range(12):
                if not clientData(0, i):
                    values.append('-')
                else:
                    values.append(clientData(0, i).text())
            else:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute('INSERT OR IGNORE INTO p_clients (tckn, name, surname, phonenumber, birthdate, height, strDate, strWeight, strBKI, strWaist, strHips, strWaistHipsRatio) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', values)
                if not connection.total_changes:
                    self.duplicateEntryError()
                else:
                    self.inputSuccessfull()
                    self.ui.tblSaveClient.clearContents()
                connection.commit()
                connection.close()
                break
        self.listClients()

    def listClients(self):
        self.ui.tblClientData.clear()
        self.tableHeaders()
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM p_clients')
        for rowIndex, rowData in enumerate(cursor):
            for columnIndex, columnData in enumerate(rowData):
                self.ui.tblClientData.setItem(
                    rowIndex, columnIndex, QtWidgets.QTableWidgetItem(str(columnData)))
        connection.commit()
        connection.close()

    def updateClient(self):
        selected = self.ui.tblClientData.selectedItems()
        if len(selected) == 12:
            answer = QMessageBox.question(
                self, 'Kaydı Güncelle', f"{selected[0].text()} tc kimlik numaralı {selected[1].text()} {selected[2].text()} kaydını güncellemek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE p_clients SET name=?, surname=?, phonenumber=?, birthdate=?, height=?, strDate=?, strWeight=?, strBKI=?, strWaist=?, strHips=?, strWaistHipsRatio=? WHERE tckn=?',
                               (selected[1].text(), selected[2].text(),
                                selected[3].text(), selected[4].text(
                               ), selected[5].text(),
                                   selected[6].text(), selected[7].text(
                               ), selected[8].text(),
                                   selected[9].text(), selected[10].text(), selected[11].text(), selected[0].text()))
                connection.commit()
                connection.close()
                self.listClients()

    def deleteEntry(self):
        selected = self.ui.tblClientData.selectedItems()
        if len(selected) == 12:
            answer = QMessageBox.question(
                self, 'Kaydı Sil', f"""{selected[0].text()} tc kimlik numaralı {selected[1].text()} {selected[2].text()} isimli kaydı silmek istiyor musunuz?""", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute("DELETE FROM clients WHERE tckn='%s'" %
                               selected[0].text())
                connection.commit()
                connection.close()
                self.listClients()

    def searchClient(self):
        searchByTckn = self.ui.lineSearchTCKN.text()
        searchByName = self.ui.lineSearchName.text()
        searchBySurname = self.ui.lineSearchSurname.text()
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * from p_clients WHERE tckn LIKE ? || '%' AND name LIKE ? || '%' AND surname LIKE ? || '%'", (
            searchByTckn, searchByName, searchBySurname))
        self.ui.tblClientData.clearContents()
        for rowIndex, rowData in enumerate(cursor):
            for columnIndex, columnData in enumerate(rowData):
                self.ui.tblClientData.setItem(
                    rowIndex, columnIndex, QtWidgets.QTableWidgetItem(str(columnData)))
        connection.commit()
        connection.close()

    # Override etmek için fonksiyon isimlerini aynı verdim.
    def show_ClientRecords(self):
        if self.PregnancyRecords is None:
            self.PregnancyRecords = PregnancyRecords()
        if self.ui.tblClientData.selectedItems():
            tckn = self.ui.tblClientData.selectedItems()[0].text()
            self.PregnancyRecords.show()
            self.PregnancyRecords.ui.clientTCKN.setText(
                self.ui.tblClientData.selectedItems()[0].text())
            self.PregnancyRecords.ui.clientName.setText(self.ui.tblClientData.selectedItems(
            )[1].text() + " " + self.ui.tblClientData.selectedItems()[2].text())
        else:
            self.selectClientError()


class ClientRecords(QtWidgets.QWidget):
    "Danışan Muyene kayıtları."

    def __init__(self):
        super(ClientRecords, self).__init__()
        self.ui = Ui_ValueForm()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle('Danışan Takip Formu')

        self.tableHeaders()
        self.createDatabase()
        self.ui.btnKayitEkle.clicked.connect(self.addRecord)
        self.ui.btnKaydiSil.clicked.connect(self.deleteEntry)
        self.ui.btnKayitListele.clicked.connect(self.listRecords)
        self.ui.btnKaydiGuncelle.clicked.connect(self.updateRecord)
        self.ui.btnKiloGrafigi.clicked.connect(self.weightGraphic)
        self.ui.btnCikis.clicked.connect(self.close)

    def createDatabase(self):
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS client_values (tckn text, date text unique, 
                kilo text, bel text, kalca text, aclikglukoz text, aclikinsulin text, homa text, 
                hba1c text, tg text, kolesterol text, ldl text, hdl text, tsh text, t4 text, 
                t3 text, alt text, ast text, urikasit text, bilirubin text, demir text, 
                ferritin text, fe text, dvit text, folik text, b12 text)''')
        connection.commit()
        connection.close()

    def listRecords(self):
        tckn = self.ui.clientTCKN.text()
        self.tableHeaders()
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM client_values WHERE tckn='%s'" % tckn)
        for rowIndex, rowData in enumerate(cursor):
            for columnIndex, columnData in enumerate(rowData):
                self.ui.tblClientValues.setItem(
                    columnIndex - 1, rowIndex + 1, QtWidgets.QTableWidgetItem(str(columnData)))
        connection.commit()
        connection.close()

    def addRecord(self):
        while True:
            values = [self.ui.clientTCKN.text()]
            clientRecord = self.ui.tblClientValues.item
            if not (clientRecord(0, 0) and clientRecord(1, 0)):
                self.recordError()
                break
            for i in range(25):
                if not clientRecord(i, 0):
                    values.append(' ')
                else:
                    values.append(clientRecord(i, 0).text())
            else:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute('''INSERT OR IGNORE INTO client_values (tckn, date, kilo, bel, kalca, aclikglukoz, aclikinsulin, 
                        homa, hba1c, tg, kolesterol, ldl, hdl, tsh, t4, t3, alt, ast, urikasit, bilirubin, demir, ferritin, fe, dvit, 
                        folik, b12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', values)
                if not connection.total_changes:
                    self.duplicateEntryError()
                else:
                    self.inputSuccessfull()
                connection.commit()
                connection.close()
                self.listRecords()
                break

    def updateRecord(self):
        selected = self.ui.tblClientValues.selectedItems()
        print(len(selected))
        if len(selected) == 25:
            answer = QMessageBox.question(
                self, 'Kaydı Güncelle', f"{selected[0].text()} tarihli kaydı güncellemek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute("""UPDATE client_values SET date=?, kilo=?, bel=?, kalca=?, aclikglukoz=?, aclikinsulin=?, homa=?,
                                    hba1c=?, tg=?, kolesterol=?, ldl=?, hdl=?, tsh=?, t4=?, t3=?, alt=?, ast=?, urikasit=?, 
                                    bilirubin=?, demir=?, ferritin=?, fe=?, dvit=?, folik=?, b12=? WHERE date=?""",
                               (selected[0].text(), selected[1].text(), selected[2].text(), selected[3].text(),
                                selected[4].text(), selected[5].text(
                               ), selected[6].text(), selected[7].text(),
                                   selected[8].text(), selected[9].text(
                               ), selected[10].text(), selected[11].text(),
                                   selected[12].text(), selected[13].text(
                               ), selected[14].text(), selected[15].text(),
                                   selected[16].text(), selected[17].text(
                               ), selected[18].text(), selected[19].text(),
                                   selected[20].text(), selected[21].text(
                               ), selected[22].text(), selected[23].text(),
                                   selected[24].text(), selected[0].text()))
                connection.commit()
                connection.close()
                self.listRecords()
        else:
            self.selectionError()

    def deleteEntry(self):
        selected = self.ui.tblClientValues.selectedItems()
        if len(selected) == 25:
            answer = QMessageBox.question(
                self, 'Kaydı Sil', f"""{selected[0].text()} tarihli kaydı silmek istiyor musunuz?""", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute(
                    "DELETE FROM client_values WHERE date='%s'" % selected[0].text())
                connection.commit()
                connection.close()
                self.listRecords()
        else:
            self.selectionError()

    def tableHeaders(self):
        self.ui.tblClientValues.clearContents()
        self.ui.tblClientValues.setItem(0, 0, QtWidgets.QTableWidgetItem(
            str(datetime.date.today().strftime("%d %B %Y"))))
        self.ui.tblClientValues.setVerticalHeaderLabels(("Muayene Tarihi", "Kilo", "Bel", "Kalça", "Açlık Glukoz (74-110)",
                                                         "Açlık İnsülin (<10)", "HOMA-IR (<2,5)", "HbA1C (4-6,20)", "TG (0-150)",
                                                         "Kolesterol (0-200)", "LDL (0-130)", "HDL (33-90)", "TSH (0,38-5,33)",
                                                         "T4 (0,61-1,12)", "T3 ( )", "ALT (SGPT) (0-35)", "AST (SGOT) (0-35)",
                                                         "Ürik Asit", "Bilirubin", "Demir (50-180)", "Ferritin (11-306)",
                                                         "Fe Bağ. Kap. (155-355)", "D Vit (30-100)", "Folik Asit", "B12"))
        self.ui.tblClientValues.setHorizontalHeaderLabels(("Muayene Ekle", "Muayene 1", "Muayene 2", "Muayene 3", "Muayene 4", "Muayene 5",
                                                           "Muayene 6", "Muayene 7", "Muayene 8", "Muayene 9", "Muayene 10",
                                                           "Muayene 11", "Muayene 12", "Muayene 13", "Muayene 14", "Muayene 15",
                                                           "Muayene 16", "Muayene 17", "Muayene 18", "Muayene 19", "Muayene 20",
                                                           "Muayene 21", "Muayene 22", "Muayene 23", "Muayene 24", "Muayene 25",
                                                           "Muayene 26", "Muayene 27", "Muayene 28", "Muayene 29", "Muayene 30",
                                                           "Muayene 31", "Muayene 32", "Muayene 33", "Muayene 34", "Muayene 35",
                                                           "Muayene 36", "Muayene 37", "Muayene 38", "Muayene 39", "Muayene 40",
                                                           "Muayene 41", "Muayene 42", "Muayene 43", "Muayene 44", "Muayene 45",
                                                           "Muayene 46", "Muayene 47", "Muayene 48", "Muayene 49"))

    def recordError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText(
            'Muayene eklemek için muayene tarihi ve sayısal bir kilo değeri giriniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def selectionError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText(
            'Silme ve güncelleme işlemi için muayene numarasını seçiniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def inputSuccessfull(self):
        msg = QMessageBox()
        msg.setWindowTitle('Kayıt Eklendi')
        msg.setText('Kaydınız başarıyla eklendi.')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def duplicateEntryError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText("Bu tarihe ait bir kayıt zaten mevcut.")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def weightGraphic(self):
        values = self.ui.tblClientValues.item
        weights = []
        dates = []
        i = 1
        while (values(0, i) and values(1, i)):
            dates.append(values(0, i).text())
            weights.append(float(values(1, i).text()))
            i += 1

        weights.reverse()
        dates.reverse()
        matplotlib.pyplot
        matplotlib.pyplot.xlabel("Tarih")
        matplotlib.pyplot.ylabel("Kilo")
        matplotlib.pyplot.plot(dates, weights, color="r",
                               marker=".", linewidth=2)

        matplotlib.pyplot.title(
            f"{self.ui.clientName.text()} Kilo Değişim Grafiği")

        matplotlib.pyplot.show()


class PregnancyRecords(QtWidgets.QWidget):
    "Gebe Danışan Muyene kayıtları."

    def __init__(self):
        super(PregnancyRecords, self).__init__()
        self.ui = Ui_PregnancyForm()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle('Gebe Takip Formu')

        self.tableHeaders()
        self.createDatabase()
        self.ui.btnKayitEkle.clicked.connect(self.addRecord)
        self.ui.btnKaydiSil.clicked.connect(self.deleteEntry)
        self.ui.btnKayitListele.clicked.connect(self.listRecords)
        self.ui.btnKaydiGuncelle.clicked.connect(self.updateRecord)
        self.ui.btnCikis.clicked.connect(self.close)

    def createDatabase(self):
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS p_client_values (tckn text, date text unique, kilo text, 
                gokilo text, gobki text, gbaslangic text, khaftalik text,
                bel text, kalca text, aclikglukoz text, aclikinsulin text, homa text, 
                hba1c text, tg text, kolesterol text, ldl text, hdl text, tsh text, t4 text, 
                t3 text, alt text, ast text, urikasit text, bilirubin text, demir text, 
                ferritin text, fe text, dvit text, folik text, b12 text)''')
        connection.commit()
        connection.close()

    def listRecords(self):
        tckn = self.ui.clientTCKN.text()
        self.tableHeaders()
        connection = sqlite3.connect('node_app.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM p_client_values WHERE tckn='%s'" % tckn)
        for rowIndex, rowData in enumerate(cursor):
            for columnIndex, columnData in enumerate(rowData):
                self.ui.tblClientValues.setItem(
                    columnIndex - 1, rowIndex + 1, QtWidgets.QTableWidgetItem(str(columnData)))
        connection.commit()
        connection.close()

    def addRecord(self):
        while True:
            values = [self.ui.clientTCKN.text()]
            clientRecord = self.ui.tblClientValues.item
            if not (clientRecord(0, 0) and clientRecord(1, 0)):
                self.recordError()
                break
            for i in range(29):
                if not clientRecord(i, 0):
                    values.append(' ')
                else:
                    values.append(clientRecord(i, 0).text())
            else:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute('''INSERT OR IGNORE INTO p_client_values (tckn, date, kilo, gokilo, gobki, gbaslangic, khaftalik, bel, 
                        kalca, aclikglukoz, aclikinsulin, homa, hba1c, tg, kolesterol, ldl, hdl, tsh, t4, t3, alt, ast, urikasit, 
                        bilirubin, demir, ferritin, fe, dvit, folik, b12) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', values)
                if not connection.total_changes:
                    self.duplicateEntryError()
                else:
                    self.inputSuccessfull()
                connection.commit()
                connection.close()
                self.listRecords()
                break

    def updateRecord(self):
        selected = self.ui.tblClientValues.selectedItems()
        print(len(selected))
        if len(selected) == 29:
            answer = QMessageBox.question(
                self, 'Kaydı Güncelle', f"{selected[0].text()} tarihli kaydı güncellemek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute("""UPDATE p_client_values SET date=?, kilo=?, gokilo=?, gobki=?, gbaslangic=?, khaftalik=?, bel=?, 
                                    kalca=?, aclikglukoz=?, aclikinsulin=?, homa=?,
                                    hba1c=?, tg=?, kolesterol=?, ldl=?, hdl=?, tsh=?, t4=?, t3=?, alt=?, ast=?, urikasit=?, 
                                    bilirubin=?, demir=?, ferritin=?, fe=?, dvit=?, folik=?, b12=? WHERE date=?""",
                               (selected[0].text(), selected[1].text(), selected[2].text(), selected[3].text(),
                                selected[4].text(), selected[5].text(
                               ), selected[6].text(), selected[7].text(),
                                   selected[8].text(), selected[9].text(
                               ), selected[10].text(), selected[11].text(),
                                   selected[12].text(), selected[13].text(
                               ), selected[14].text(), selected[15].text(),
                                   selected[16].text(), selected[17].text(
                               ), selected[18].text(), selected[19].text(),
                                   selected[20].text(), selected[21].text(
                               ), selected[22].text(), selected[23].text(),
                                   selected[24].text(), selected[25].text(
                               ), selected[26].text(), selected[27].text(),
                                   selected[28].text(), selected[0].text()))
                connection.commit()
                connection.close()
                self.listRecords()
        else:
            self.selectionError()

    def deleteEntry(self):
        selected = self.ui.tblClientValues.selectedItems()
        if len(selected) == 29:
            answer = QMessageBox.question(
                self, 'Kaydı Sil', f"""{selected[0].text()} tarihli kaydı silmek istiyor musunuz?""", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                connection = sqlite3.connect('node_app.db')
                cursor = connection.cursor()
                cursor.execute(
                    "DELETE FROM p_client_values WHERE date='%s'" % selected[0].text())
                connection.commit()
                connection.close()
                self.listRecords()

    def tableHeaders(self):
        self.ui.tblClientValues.clearContents()
        self.ui.tblClientValues.setItem(0, 0, QtWidgets.QTableWidgetItem(
            str(datetime.date.today().strftime("%d %B %Y"))))
        self.ui.tblClientValues.setVerticalHeaderLabels(("Muayene Tarihi", "Kilo", "G.Ö. Kilo", "G.Ö. BKI", "Gebelik Başlangıç",
                                                         "Kaç Haftalık", "Bel", "Kalça", "Açlık Glukoz (74-110)",
                                                         "Açlık İnsülin (<10)", "HOMA-IR (<2,5)", "HbA1C (4-6,20)", "TG (0-150)",
                                                         "Kolesterol (0-200)", "LDL (0-130)", "HDL (33-90)", "TSH (0,38-5,33)",
                                                         "T4 (0,61-1,12)", "T3 ( )", "ALT (SGPT) (0-35)", "AST (SGOT) (0-35)",
                                                         "Ürik Asit", "Bilirubin", "Demir (50-180)", "Ferritin (11-306)",
                                                         "Fe Bağ. Kap. (155-355)", "D Vit (30-100)", "Folik Asit", "B12"))
        self.ui.tblClientValues.setHorizontalHeaderLabels(("Muayene Ekle", "Muayene 1", "Muayene 2", "Muayene 3", "Muayene 4", "Muayene 5",
                                                           "Muayene 6", "Muayene 7", "Muayene 8", "Muayene 9", "Muayene 10",
                                                           "Muayene 11", "Muayene 12", "Muayene 13", "Muayene 14", "Muayene 15",
                                                           "Muayene 16", "Muayene 17", "Muayene 18", "Muayene 19", "Muayene 20",
                                                           "Muayene 21", "Muayene 22", "Muayene 23", "Muayene 24", "Muayene 25",
                                                           "Muayene 26", "Muayene 27", "Muayene 28", "Muayene 29", "Muayene 30",
                                                           "Muayene 31", "Muayene 32", "Muayene 33", "Muayene 34", "Muayene 35",
                                                           "Muayene 36", "Muayene 37", "Muayene 38", "Muayene 39", "Muayene 40",
                                                           "Muayene 41", "Muayene 42", "Muayene 43", "Muayene 44", "Muayene 45",
                                                           "Muayene 46", "Muayene 47", "Muayene 48", "Muayene 49"))

    def recordError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText('Muayene eklemek için muayene tarihi ve kilo giriniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def selectionError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText(
            'Silme ve güncelleme işlemi için muayene numarasını seçiniz.')
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def inputSuccessfull(self):
        msg = QMessageBox()
        msg.setWindowTitle('Kayıt Eklendi')
        msg.setText('Kaydınız başarıyla eklendi.')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def duplicateEntryError(self):
        msg = QMessageBox()
        msg.setWindowTitle('Hata')
        msg.setText("Bu tarihe ait bir kayıt zaten mevcut.")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = DiyetApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app()
