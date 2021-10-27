from plantilla_admin import Ui_MainWindow
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
        self.pushButton_5.clicked.connect(self.Abrir_Ventana_Historiales)
        self.pushButton_3.clicked.connect(self.Abrir_Ventana_Doctores)
        self.pushButton_6.clicked.connect(self.Abrir_Ventana_Pacientes)
        self.pushButton_10.clicked.connect(self.Abrir_Ventana_Administrador)
        self.pushButton_2.clicked.connect(self.Mostrar_Paciente)

    def Abrir_Ventana_Inicio(self):
        self.tabWidget.setCurrentIndex(0)

    def Abrir_Ventana_Doctores(self):
        self.tabWidget.setCurrentIndex(1)

    def Abrir_Ventana_Historiales(self):
        self.tabWidget.setCurrentIndex(2)

    def Abrir_Ventana_Administrador(self):
        self.tabWidget.setCurrentIndex(3)

    def Abrir_Ventana_Pacientes(self):
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

def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
