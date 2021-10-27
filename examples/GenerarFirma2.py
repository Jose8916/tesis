from plantilla_segunda import Ui_MainWindow
from ingreso import Ui_Form

from OpenSSL.crypto import load_pkcs12
from endesive.pdf import pdf
from PyQt5.QtWidgets import *
import sqlite3

import os

import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

import sys
sys.path.append('C:/Users/Usuario/Desktop/PROYECTO_TESIS_V3')

class Login(QWidget, Ui_Form):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)

    def Handel_Login(self):
        conexion = sqlite3.connect("Proyecto.db")
        cursor = conexion.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = '''SELECT * FROM usuarios'''

        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            if username == row[1] and password == row[2]:
                print('user match')
                self.window2 = MainApp()
                self.close()
                self.window2.show()

            else:
                self.label.setText('Asegurese de haber ingresado su usuario y clave correctamente ')

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.tabWidget.tabBar().setVisible(False)

        self.MostrarHistoriales()

    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.AgregarHistorial)
        self.pushButton_5.clicked.connect(self.Abrir_Ventana_Redaccion)
        self.pushButton_3.clicked.connect(self.Abrir_Ventana_Documentos)
        # self.pushButton_4.clicked.connect(self.Abrir_Ventana_Inicio)
        self.pushButton_6.clicked.connect(self.Abrir_Ventana_Vista_Doctor)
        self.pushButton_10.clicked.connect(self.Abrir_Ventana_Vista_Pacientes)

        self.pushButton_2.clicked.connect(self.Mostrar_Paciente)

    def Abrir_Ventana_Inicio(self):
        self.tabWidget.setCurrentIndex(0)

    def Abrir_Ventana_Redaccion(self):
        self.tabWidget.setCurrentIndex(1)

    def Abrir_Ventana_Documentos(self):
        self.tabWidget.setCurrentIndex(2)

    def Abrir_Ventana_Vista_Doctor(self):
        self.tabWidget.setCurrentIndex(3)

    def Abrir_Ventana_Vista_Pacientes(self):
        self.tabWidget.setCurrentIndex(4)

    def ShowPdf(self):
         path = '5.pdf'
         os.system(path)

    def MostrarHistoriales(self):

        conexion = sqlite3.connect("Proyecto.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT codigo_historial, nombre_doctor, nombre_paciente, sintomas, tratamiento, fecha, documento  FROM historiales")

        data = cursor.fetchall()
        print(data)
        if data:

            self.tableWidget.setRowCount(0)

            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

        self.tableWidget.cellClicked.connect(self.ShowPdf)

    def Mostrar_Paciente(self):
        conexion = sqlite3.connect("Proyecto.db")
        cursor = conexion.cursor()

        nombre_a_buscar = self.comboBox_2.currentText()

        cursor.execute("SELECT * FROM pacienteshistorial WHERE nombre = '%s'" % nombre_a_buscar)
        # sql = '''SELECT * FROM pacienteshistorial WHERE nombre = '%s' '''
        # cursor.execute(sql, nombre_a_buscar)

        data = cursor.fetchone()

        self.lineEdit_28.setText(data[1])
        self.lineEdit_24.setText(data[7])
        self.lineEdit_29.setText(data[3])
        self.lineEdit_23.setText(data[4])
        self.lineEdit_22.setText(data[5])
        self.lineEdit_25.setText(data[8])
        self.lineEdit_26.setText(str(data[2]))
        self.lineEdit_27.setText(str(data[9]))
        self.lineEdit_30.setText(str(data[10]))


    def AgregarHistorial(self):
        conexion = sqlite3.connect("Proyecto.db")
        cursor = conexion.cursor()

        codhis = self.lineEdit_6.text()
        nomdoc = self.lineEdit_8.text()
        fecha = self.lineEdit_4.text()
        nombrep = self.comboBox.currentText()
        edadp = self.lineEdit_2.text()
        sexop = self.lineEdit_3.text()

        alergiasp = self.textEdit_4.toPlainText()
        antecedentesp = self.textEdit_5.toPlainText()
        sintomasp = self.textEdit_2.toPlainText()
        antecedentesfamiliaresp = self.textEdit_7.toPlainText()
        medicacionp = self.textEdit_6.toPlainText()
        diagnosticop = self.textEdit_3.toPlainText()
        tratamientop = self.textEdit_8.toPlainText()

        documento = codhis + '.pdf'

        datos = [codhis, nomdoc, fecha, nombrep, edadp, sexop, alergiasp, antecedentesp, antecedentesfamiliaresp,
                 medicacionp, sintomasp, diagnosticop, tratamientop, documento]

        cursor.execute(
            "INSERT INTO historiales (codigo_historial, nombre_doctor, fecha, nombre_paciente, edad, sexo, alergias, antecedentes, antecedentes_familiares, medicacion, sintomas, diagnostico, tratamiento, documento)"
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", datos)

        self.statusBar().showMessage('Historial Generado', 2000)

        conexion.commit()

        date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
        date = date.strftime('%Y%m%d%H%M%S+00\'00\'')
        date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
        date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
        dct = {
            "aligned": 0,
            "sigflags": 3,
            "sigflagsft": 132,
            "sigpage": 0,
            "sigbutton": True,
            "sigfield": "Firma",
            "sigandcertify": True,
            "signaturebox": (100, 50, 250, 100),
            "signature": "Dr. Martin Apaza Quispe,  Cod: 874478",
            "contact": "mak@trisoft.com.pl",
            "location": "Lima - Peru",
            "signingdate": date,
            "reason": "Validacion de la firma",
            "password": "1234",
        }
        p12 = load_pkcs12(open('demo2_user2.p12', 'rb').read(), '1234')
        doc = pdf.FPDF()
        doc.pkcs11_setup(dct,
                         p12.get_privatekey().to_cryptography_key(),
                         p12.get_certificate().to_cryptography(),
                         [],
                         'sha256'
                         )

        doc.add_page()

        # fpdf.image(name, x = None, y = None, w = 0, h = 0, type = '', link = '')
        doc.image('logohospital.png', 90, 5, 20, 20, type='', link='')

        # x, y, w, h
        doc.rect(14, 57, 172, 25, style='')

        doc.rect(14, 86.5, 172, 50.5, style='')

        doc.rect(14, 141.5, 172, 90.5, style='')


        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=160.0, h=10.0, align='R', txt='Fecha:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=fecha, border=0, ln=1)

        doc.set_font('Arial', 'BU', 1.0)
        doc.cell(w=180.0, h=15.0, align='C', txt='', border=0, ln=1)

        doc.set_font('Arial', 'BU', 15.0)
        doc.cell(w=180.0, h=15.0, align='C', txt='HISTORIAL MEDICO DEL PACIENTE', border=0, ln=1)

        doc.set_font('Arial', 'BU', 10.0)
        doc.cell(w=180.0, h=10.0, align='C', txt='                                                                                                                                                                              ', border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=10.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=20.0, h=7.0, align='L', txt='Código:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=60.0, h=7.0, align='L', txt='HC-N°' + codhis, border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=10.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=20.0, h=10.0, align='L', txt='Doctor:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=nomdoc, border=0, ln=1)

        doc.set_font('Arial', 'BU', 10.0)
        doc.cell(w=180.0, h=5.0, align='C', txt='                                                                                                                                                                              ', border=0, ln=1)

        doc.set_font('Arial', 'BU', 10.0)
        doc.cell(w=180.0, h=5.0, align='C', txt='                                                                                                                                                                              ', border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=10.0, h=7.0, align='L')
        doc.set_font('Arial', 'BU', 13.0)
        doc.cell(w=30.0, h=15.0, align='L', txt='INFORMACION DEL PACIENTE', border=0, ln=1)

        doc.set_font('Arial', 'B', 20.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=23.0, h=10.0, align='L', txt='Paciente:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=nombrep, border=0, ln=1)

        doc.set_font('Arial', 'B', 20.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=23.0, h=10.0, align='L', txt='Edad:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=edadp + ' años', border=0, ln=1)

        doc.set_font('Arial', 'B', 20.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=23.0, h=10.0, align='L', txt='Sexo:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=sexop, border=0, ln=1)

        doc.set_font('Arial', 'BU', 10.0)
        doc.cell(w=180.0, h=5.0, align='C', txt='                                                                                                                                                                              ', border=0, ln=1)

        doc.set_font('Arial', 'BU', 10.0)
        doc.cell(w=180.0, h=5.0, align='C', txt='                                                                                                                                                                              ', border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=10.0, h=7.0, align='L')
        doc.set_font('Arial', 'BU', 13.0)
        doc.cell(w=30.0, h=15.0, align='L', txt='INFORMACION MEDICA', border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=60.0, h=10.0, align='L', txt='Alergias:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=alergiasp, border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=60.0, h=10.0, align='L', txt='Antecedentes:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=antecedentesp, border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=60.0, h=10.0, align='L', txt='Antecedentes Familiares:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=antecedentesfamiliaresp, border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=60.0, h=10.0, align='L', txt='Síntomas:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=sintomasp, border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=60.0, h=10.0, align='L', txt='Medicacion Previa:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=medicacionp, border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=60.0, h=10.0, align='L', txt='Diagnóstico:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=diagnosticop, border=0, ln=1)

        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=15.0, h=7.0, align='L')
        doc.set_font('Arial', 'B', 13.0)
        doc.cell(w=60.0, h=10.0, align='L', txt='Tratamiento:', border=0, ln=0)
        doc.set_font('Arial', 'U', 13.0)
        doc.cell(w=80.0, h=10.0, align='L', txt=tratamientop, border=0, ln=1)

        doc.set_font('Arial', 'BU', 10.0)
        doc.cell(w=180.0, h=5.0, align='C', txt='                                                                                                                                                                              ', border=0, ln=1)

        doc.footer()

        doc.output(codhis + '.pdf', "F")

        with open("demo2_user1.p12", "rb") as fp:
            p12 = pkcs12.load_key_and_certificates(
                fp.read(), b"1234", backends.default_backend()
            )
        fname = codhis + '.pdf'
        if len(sys.argv) > 1:
            fname = sys.argv[1]
        datau = open(fname, "rb").read()
        datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
        fname = fname.replace(codhis + '.pdf', codhis + '.pdf')
        with open(fname, "wb") as fp:
            fp.write(datau)
            fp.write(datas)

        codhis = int(codhis) + 1


        self.comboBox.setCurrentIndex(0)
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_6.setText(str(codhis))
        self.textEdit_4.setText('')
        self.textEdit_5.setText('')
        self.textEdit_2.setText('')
        self.textEdit_7.setText('')
        self.textEdit_6.setText('')
        self.textEdit_3.setText('')
        self.textEdit_8.setText('')

        path = fname
        os.system(path)

        self.MostrarHistoriales()

def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
