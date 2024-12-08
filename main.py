# import sys
# import os
# from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
# from services.folder_service import FolderProcessor
# from utils.setup_utils import install_tesseract  # Función comentada para instalar Tesseract
# from utils.app_logger import setup_logging
# from ui.layout import create_main_layout
# from ui.mainwindow import Ui_MainWindow 

# # Configurar logging
# setup_logging()
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)

#         # Variables para almacenar la carpeta, año y mes seleccionados
#         self.selected_folder = ""
#         self.selected_year = ""
#         self.selected_month = ""

#         # Conectar botones a funciones
#         self.ui.pushButton.clicked.connect(self.select_folder)
#         self.ui.pushButton_2.clicked.connect(self.start_process)

#         # Tamaño fijo de la ventana
#         self.setFixedSize(300, 300)

#     def select_folder(self):
#         """Abre un cuadro de diálogo para seleccionar la carpeta padre."""
#         folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta Padre")
#         if folder:
#             self.selected_folder = folder
#             print(f"Carpeta seleccionada: {folder}")

#     def start_process(self):
#         """Lógica para recorrer carpetas y procesar archivos."""
#         self.selected_year = self.ui.yearComboBox.currentText()
#         self.selected_month = self.ui.comboBox.currentText()

#         # Validar selecciones
#         if self.selected_year == "Seleccionar Año" or self.selected_month == "Seleccionar mes":
#             QMessageBox.warning(self, "Advertencia", "Por favor selecciona un año y un mes válidos.")
#             return

#         if not self.selected_folder:
#             QMessageBox.warning(self, "Advertencia", "Por favor selecciona una carpeta primero.")
#             return

#         # Ingresar en las carpetas y procesar los archivos
#         self.process_files()

#     def process_files(self):
#         """Procesa las carpetas y archivos según el año y mes seleccionados."""
#         payroll_folder_name = f"Payroll {self.selected_year}"
#         year_folder_name = f"{self.selected_year}"

#         # Iterar sobre las subcarpetas en la carpeta seleccionada
#         for client_folder in os.listdir(self.selected_folder):
#             client_path = os.path.join(self.selected_folder, client_folder)

#             # Verificar si es una carpeta
#             if not os.path.isdir(client_path):
#                 continue

#             # Intentar acceder a "Payroll {Año}" o "{Año}"
#             payroll_path = os.path.join(client_path, payroll_folder_name)
#             year_path = os.path.join(client_path, year_folder_name)

#             if os.path.exists(payroll_path):
#                 target_path = payroll_path
#             elif os.path.exists(year_path):
#                 target_path = year_path
#             else:
#                 print(f"No se encontró una carpeta válida en: {client_path}")
#                 continue

#             print(f"Ingresando a carpeta: {target_path}")

#             # Recorrer los archivos por semana
#             self.process_weekly_files(target_path)

#     def process_weekly_files(self, folder_path):
#         """Procesa los archivos dentro de una carpeta dada."""
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)

#             # Verificar si es un archivo y cumple con los criterios
#             if os.path.isfile(file_path):
#                 # Verificar si el archivo finaliza con EDD, 941 o tiene la fecha (Check Date)
#                 if file_name.endswith("EDD") or file_name.endswith("941") or self.is_weekly_file(file_name):
#                     print(f"Archivo válido encontrado: {file_path}")

#     def is_weekly_file(self, file_name):
#         """Verifica si un archivo tiene formato de semana, por ejemplo: 01112024."""
#         # Verificar que el archivo tenga exactamente 8 caracteres antes de la extensión
#         if len(file_name.split(".")[0]) == 8:
#             # Validar que los primeros 6 caracteres sean una fecha válida (ddmmyyyy)
#             try:
#                 day, month, year = int(file_name[:2]), int(file_name[2:4]), int(file_name[4:8])
#                 if 1 <= day <= 31 and 1 <= month <= 12 and int(self.selected_year) == year:
#                     return True
#             except ValueError:
#                 pass
#         return False

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from services.folder_service import FolderProcessor
from utils.app_logger import setup_logging
from ui.mainwindow import Ui_MainWindow

# Configurar logging
setup_logging()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables para almacenar la carpeta, año y mes seleccionados
        self.selected_folder = None
        self.selected_year = ""
        self.selected_month = ""

        # Conectar botones a funciones
        self.ui.pushButton.clicked.connect(self.select_folder)
        self.ui.pushButton_2.clicked.connect(self.start_process)

        # Tamaño fijo de la ventana
        self.setFixedSize(300, 300)

    def select_folder(self):
        """Abre un cuadro de diálogo para seleccionar la carpeta padre."""
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta Padre")
        if folder:
            self.selected_folder = folder
            print(f"Carpeta seleccionada: {folder}")

    def start_process(self):
        """Lógica para recorrer carpetas y procesar archivos."""
        self.selected_year = self.ui.yearComboBox.currentText()
        self.selected_month = self.ui.comboBox.currentText()

        # Validar selecciones
        if self.selected_year == "Seleccionar Año" or self.selected_month == "Seleccionar mes":
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un año y un mes válidos.")
            return

        if not self.selected_folder:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una carpeta primero.")
            return

        # Procesar carpetas
        folder_processor = FolderProcessor()
        folder_processor.process(self.selected_folder, self.selected_year, self.selected_month)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
