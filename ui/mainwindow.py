# # # -*- coding: utf-8 -*-

# # # Form implementation generated from reading ui file 'mainwindow.ui'
# # #
# # # Created by: PyQt5 UI code generator 5.15.11
# # #
# # # WARNING: Any manual changes made to this file will be lost when pyuic5 is
# # # run again.  Do not edit this file unless you know what you are doing.


# # from PyQt5 import QtCore, QtGui, QtWidgets


# # class Ui_MainWindow(object):
# #     def setupUi(self, MainWindow):
# #         MainWindow.setObjectName("MainWindow")
# #         MainWindow.setEnabled(True)
# #         MainWindow.resize(300, 400)
# #         MainWindow.setAutoFillBackground(True)
# #         self.centralwidget = QtWidgets.QWidget(MainWindow)
# #         self.centralwidget.setObjectName("centralwidget")
# #         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
# #         self.pushButton.setGeometry(QtCore.QRect(50, 20, 201, 37))
# #         self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
# #         self.pushButton.setAutoFillBackground(False)
# #         self.pushButton.setStyleSheet("QPushButton {\n"
# # "    background-color: #3498db; /* Azul moderno */\n"
# # "    color: white;\n"
# # "    font-size: 16px;\n"
# # "    border-radius: 10px;\n"
# # "    padding: 8px;\n"
# # "}\n"
# # "QPushButton:hover {\n"
# # "    background-color: #2980b9;\n"
# # "}\n"
# # "QComboBox {\n"
# # "    background-color: white;\n"
# # "    color: #2c3e50;\n"
# # "    border: 1px solid #3498db;\n"
# # "    font-size: 14px;\n"
# # "    padding: 5px;\n"
# # "}\n"
# # "QProgressBar {\n"
# # "    border: 1px solid #3498db;\n"
# # "    border-radius: 5px;\n"
# # "    background-color: #ecf0f1;\n"
# # "    text-align: center;\n"
# # "    font-size: 14px;\n"
# # "}\n"
# # "QProgressBar::chunk {\n"
# # "    background-color: #27ae60; /* Verde progresivo */\n"
# # "    width: 20px;\n"
# # "}\n"
# # "")
# #         icon = QtGui.QIcon()
# #         icon.addPixmap(QtGui.QPixmap("../../Freelance/Diseño PDF/Iconos/Seleccionar_carpeta.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
# #         self.pushButton.setIcon(icon)
# #         self.pushButton.setCheckable(True)
# #         self.pushButton.setChecked(True)
# #         self.pushButton.setAutoRepeat(True)
# #         self.pushButton.setAutoExclusive(True)
# #         self.pushButton.setAutoRepeatDelay(3000)
# #         self.pushButton.setAutoRepeatInterval(1000)
# #         self.pushButton.setAutoDefault(True)
# #         self.pushButton.setDefault(True)
# #         self.pushButton.setFlat(True)
# #         self.pushButton.setObjectName("pushButton")
# #         self.yearComboBox = QtWidgets.QComboBox(self.centralwidget)
# #         self.yearComboBox.setGeometry(QtCore.QRect(50, 80, 201, 24))
# #         self.yearComboBox.setAccessibleName("")
# #         self.yearComboBox.setEditable(False)
# #         self.yearComboBox.setObjectName("yearComboBox")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.yearComboBox.addItem("")
# #         self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
# #         self.pushButton_2.setGeometry(QtCore.QRect(50, 230, 201, 24))
# #         self.pushButton_2.setCheckable(False)
# #         self.pushButton_2.setObjectName("pushButton_2")
# #         self.comboBox = QtWidgets.QComboBox(self.centralwidget)
# #         self.comboBox.setGeometry(QtCore.QRect(50, 130, 201, 24))
# #         self.comboBox.setMinimumSize(QtCore.QSize(72, 0))
# #         self.comboBox.setObjectName("comboBox")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.comboBox.addItem("")
# #         self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
# #         self.pushButton_3.setEnabled(False)
# #         self.pushButton_3.setGeometry(QtCore.QRect(50, 180, 201, 24))
# #         self.pushButton_3.setCheckable(False)
# #         self.pushButton_3.setObjectName("pushButton_3")
# #         self.comboBox.raise_()
# #         self.pushButton.raise_()
# #         self.yearComboBox.raise_()
# #         self.pushButton_2.raise_()
# #         self.pushButton_3.raise_()
# #         MainWindow.setCentralWidget(self.centralwidget)
# #         self.menubar = QtWidgets.QMenuBar(MainWindow)
# #         self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
# #         self.menubar.setObjectName("menubar")
# #         MainWindow.setMenuBar(self.menubar)
# #         self.statusbar = QtWidgets.QStatusBar(MainWindow)
# #         self.statusbar.setObjectName("statusbar")
# #         MainWindow.setStatusBar(self.statusbar)

# #         self.retranslateUi(MainWindow)
# #         QtCore.QMetaObject.connectSlotsByName(MainWindow)

# #     def retranslateUi(self, MainWindow):
# #         _translate = QtCore.QCoreApplication.translate
# #         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
# #         self.pushButton.setText(_translate("MainWindow", "Seleccionar Carpeta"))
# #         self.yearComboBox.setItemText(0, _translate("MainWindow", "Seleccionar Año"))
# #         self.yearComboBox.setItemText(1, _translate("MainWindow", "2000"))
# #         self.yearComboBox.setItemText(2, _translate("MainWindow", "2001"))
# #         self.yearComboBox.setItemText(3, _translate("MainWindow", "2002"))
# #         self.yearComboBox.setItemText(4, _translate("MainWindow", "2003"))
# #         self.yearComboBox.setItemText(5, _translate("MainWindow", "2004"))
# #         self.yearComboBox.setItemText(6, _translate("MainWindow", "2005"))
# #         self.yearComboBox.setItemText(7, _translate("MainWindow", "2006"))
# #         self.yearComboBox.setItemText(8, _translate("MainWindow", "2007"))
# #         self.yearComboBox.setItemText(9, _translate("MainWindow", "2008"))
# #         self.yearComboBox.setItemText(10, _translate("MainWindow", "2009"))
# #         self.yearComboBox.setItemText(11, _translate("MainWindow", "2010"))
# #         self.yearComboBox.setItemText(12, _translate("MainWindow", "2011"))
# #         self.yearComboBox.setItemText(13, _translate("MainWindow", "2012"))
# #         self.yearComboBox.setItemText(14, _translate("MainWindow", "2013"))
# #         self.yearComboBox.setItemText(15, _translate("MainWindow", "2014"))
# #         self.yearComboBox.setItemText(16, _translate("MainWindow", "2015"))
# #         self.yearComboBox.setItemText(17, _translate("MainWindow", "2016"))
# #         self.yearComboBox.setItemText(18, _translate("MainWindow", "2017"))
# #         self.yearComboBox.setItemText(19, _translate("MainWindow", "2018"))
# #         self.yearComboBox.setItemText(20, _translate("MainWindow", "2019"))
# #         self.yearComboBox.setItemText(21, _translate("MainWindow", "2020"))
# #         self.yearComboBox.setItemText(22, _translate("MainWindow", "2021"))
# #         self.yearComboBox.setItemText(23, _translate("MainWindow", "2022"))
# #         self.yearComboBox.setItemText(24, _translate("MainWindow", "2023"))
# #         self.yearComboBox.setItemText(25, _translate("MainWindow", "2024"))
# #         self.yearComboBox.setItemText(26, _translate("MainWindow", "2025"))
# #         self.yearComboBox.setItemText(27, _translate("MainWindow", "2026"))
# #         self.yearComboBox.setItemText(28, _translate("MainWindow", "2027"))
# #         self.yearComboBox.setItemText(29, _translate("MainWindow", "2028"))
# #         self.yearComboBox.setItemText(30, _translate("MainWindow", "2029"))
# #         self.yearComboBox.setItemText(31, _translate("MainWindow", "2030"))
# #         self.pushButton_2.setText(_translate("MainWindow", "Iniciar Proceso"))
# #         self.comboBox.setItemText(0, _translate("MainWindow", "Seleccionar mes"))
# #         self.comboBox.setItemText(1, _translate("MainWindow", "Enero"))
# #         self.comboBox.setItemText(2, _translate("MainWindow", "Febrero"))
# #         self.comboBox.setItemText(3, _translate("MainWindow", "Marzo"))
# #         self.comboBox.setItemText(4, _translate("MainWindow", "Abril"))
# #         self.comboBox.setItemText(5, _translate("MainWindow", "Mayo"))
# #         self.comboBox.setItemText(6, _translate("MainWindow", "Junio"))
# #         self.comboBox.setItemText(7, _translate("MainWindow", "Julio"))
# #         self.comboBox.setItemText(8, _translate("MainWindow", "Agosto"))
# #         self.comboBox.setItemText(9, _translate("MainWindow", "Septiembre"))
# #         self.comboBox.setItemText(10, _translate("MainWindow", "Octubre"))
# #         self.comboBox.setItemText(11, _translate("MainWindow", "Noviembre"))
# #         self.comboBox.setItemText(12, _translate("MainWindow", "Diciembre"))
# #         self.pushButton_3.setText(_translate("MainWindow", "Master"))

# from PyQt5 import QtCore, QtGui, QtWidgets


# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(300, 300)
#         MainWindow.setFixedSize(300, 300)  # Tamaño fijo de la ventana
#         MainWindow.setStyleSheet("background-color: #2c3e50;")  # Fondo gris oscuro

#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")

#         # Botón Seleccionar Carpeta
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(50, 20, 201, 37))
#         self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
#         self.pushButton.setStyleSheet("""
#             QPushButton {
#                 background-color: #3498db; /* Azul moderno */
#                 color: white;
#                 font-size: 16px;
#                 border-radius: 10px;
#                 padding: 8px;
#             }
#             QPushButton:hover {
#                 background-color: #2980b9;
#             }
#         """)
#         self.pushButton.setObjectName("pushButton")
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap("Iconos/Seleccionar_carpeta.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.pushButton.setIcon(icon)

#         # ComboBox Selección de Año
#         self.yearComboBox = QtWidgets.QComboBox(self.centralwidget)
#         self.yearComboBox.setGeometry(QtCore.QRect(50, 80, 201, 24))
#         self.yearComboBox.setEditable(False)
#         self.yearComboBox.setObjectName("yearComboBox")
#         self.yearComboBox.addItem("Seleccionar Año")
#         self.yearComboBox.addItems([str(year) for year in range(2000, 2031)])  # Añadir años dinámicamente
#         self.yearComboBox.setStyleSheet("""
#             QComboBox {
#                 background-color: white;
#                 color: #2c3e50;
#                 font-size: 14px;
#                 border: 1px solid #3498db;
#                 padding: 4px;
#             }
#             QComboBox::drop-down {
#                 border: none;
#             }
#             QComboBox:hover {
#                 border: 1px solid #2980b9;
#             }
#         """)

#         # ComboBox Selección de Mes
#         self.comboBox = QtWidgets.QComboBox(self.centralwidget)
#         self.comboBox.setGeometry(QtCore.QRect(50, 130, 201, 24))
#         self.comboBox.setObjectName("comboBox")
#         self.comboBox.addItem("Seleccionar mes")
#         self.comboBox.addItems([
#             "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
#             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
#         ])  # Añadir meses dinámicamente
#         self.comboBox.setStyleSheet("""
#             QComboBox {
#                 background-color: white;
#                 color: #2c3e50;
#                 font-size: 14px;
#                 border: 1px solid #3498db;
#                 padding: 4px;
#             }
#             QComboBox::drop-down {
#                 border: none;
#             }
#             QComboBox:hover {
#                 border: 1px solid #2980b9;
#             }
#         """)

#         # Botón Iniciar Proceso
#         self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton_2.setGeometry(QtCore.QRect(50, 180, 201, 24))
#         self.pushButton_2.setObjectName("pushButton_2")
#         self.pushButton_2.setText("Iniciar Proceso")
#         self.pushButton_2.setStyleSheet("""
#             QPushButton {
#                 background-color: #2ecc71; /* Verde moderno */
#                 color: white;
#                 font-size: 14px;
#                 border-radius: 8px;
#                 padding: 6px;
#             }
#             QPushButton:hover {
#                 background-color: #27ae60;
#             }
#         """)

#         # Configuración de la ventana principal
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)

#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "Procesamiento_PDF"))
#         self.pushButton.setText(_translate("MainWindow", "Seleccionar Carpeta"))

#     def iniciar_proceso(self):
#         """Función para manejar el inicio del proceso."""
#         year = self.yearComboBox.currentText()
#         month = self.comboBox.currentText()

#         # Validar las selecciones y mostrar mensajes de advertencia
#         if year == "Seleccionar Año" and month == "Seleccionar mes":
#             QtWidgets.QMessageBox.warning(
#                 self.centralwidget,
#                 "Advertencia",
#                 "Por favor, selecciona un año y un mes válidos."
#             )
#         elif year == "Seleccionar Año":
#             QtWidgets.QMessageBox.warning(
#                 self.centralwidget,
#                 "Advertencia",
#                 "Por favor, selecciona un año válido."
#             )
#         elif month == "Seleccionar mes":
#             QtWidgets.QMessageBox.warning(
#                 self.centralwidget,
#                 "Advertencia",
#                 "Por favor, selecciona un mes válido."
#             )
#         else:
#             QtWidgets.QMessageBox.information(
#                 self.centralwidget,
#                 "Éxito",
#                 f"Procesando para el año {year} y el mes {month}..."
#             )

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 350)
        MainWindow.setFixedSize(300, 350)  # Tamaño fijo de la ventana
        MainWindow.setStyleSheet("background-color: #2c3e50;")  # Fondo gris oscuro

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Botón Seleccionar Carpeta
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 20, 201, 37))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db; /* Azul moderno */
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.pushButton.setObjectName("pushButton")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Iconos/Seleccionar_carpeta.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)

        # ComboBox Selección de Año
        self.yearComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.yearComboBox.setGeometry(QtCore.QRect(50, 80, 201, 24))
        self.yearComboBox.setEditable(False)
        self.yearComboBox.setObjectName("yearComboBox")
        self.yearComboBox.addItem("Seleccionar Año")
        self.yearComboBox.addItems([str(year) for year in range(2000, 2031)])  # Añadir años dinámicamente
        self.yearComboBox.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #2c3e50;
                font-size: 14px;
                border: 1px solid #3498db;
                padding: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox:hover {
                border: 1px solid #2980b9;
            }
        """)

        # ComboBox Selección de Mes
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 130, 201, 24))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Seleccionar mes")
        self.comboBox.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])  # Añadir meses dinámicamente
        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #2c3e50;
                font-size: 14px;
                border: 1px solid #3498db;
                padding: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox:hover {
                border: 1px solid #2980b9;
            }
        """)

        # Botón Iniciar Proceso
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 180, 201, 24))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Iniciar Proceso")
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; /* Verde moderno */
                color: white;
                font-size: 14px;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        # Barra de Progreso
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(50, 230, 201, 24))
        self.progress_bar.setProperty("value", 0)  # Valor inicial
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #ecf0f1;
                text-align: center;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #27ae60; /* Verde progresivo */
                width: 20px;
            }
        """)

        # Configuración de la ventana principal
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Procesamiento_PDF"))
        self.pushButton.setText(_translate("MainWindow", "Seleccionar Carpeta"))
