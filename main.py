import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressBar, QStatusBar
from PyQt5.QtCore import QThread, pyqtSignal
from services.folder_service import FolderProcessor
from utils.app_logger import setup_logging
from ui.mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets

# Configurar logging
setup_logging()

class Worker(QThread):
    progressChanged = pyqtSignal(int)
    processCompleted = pyqtSignal()

    def __init__(self, folder_processor, selected_folder, selected_year, selected_month):
        super().__init__()
        self.folder_processor = folder_processor
        self.selected_folder = selected_folder
        self.selected_year = selected_year
        self.selected_month = selected_month

        # Conectar señal de FolderProcessor a la propia señal de Worker
        self.folder_processor.progressChanged.connect(self.progressChanged.emit)

    def run(self):
        self.folder_processor.process(self.selected_folder, self.selected_year, self.selected_month)
        self.processCompleted.emit()

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

        # Añadir la barra de progreso en la status bar
        self.progress_bar = QProgressBar(self)
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

        # Crear la barra de estado
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.addWidget(self.progress_bar)

    def select_folder(self):
        """
        Abre un cuadro de diálogo para seleccionar la carpeta principal.
        """
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta Padre")
        if folder:
            self.selected_folder = folder
            print(f"Carpeta seleccionada: {folder}")

    def start_process(self):
        """
        Lógica para recorrer carpetas y procesar archivos.
        """
        self.selected_year = self.ui.yearComboBox.currentText()
        self.selected_month = self.ui.comboBox.currentText()

        # Validar selecciones
        if self.selected_year == "Seleccionar Año" or self.selected_month == "Seleccionar mes":
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un año y un mes válidos.")
            return

        if not self.selected_folder:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una carpeta primero.")
            return

        # Usar la carpeta seleccionada como carpeta de salida y definir el archivo de salida
        output_folder = self.selected_folder
        output_file = "datos_combinados.xlsx"

        # Crear y configurar el procesador de carpetas
        self.folder_processor = FolderProcessor(output_folder, output_file)

        # Crear y configurar el trabajador
        self.worker = Worker(self.folder_processor, self.selected_folder, self.selected_year, self.selected_month)
        self.worker.progressChanged.connect(self.update_progress)
        self.worker.processCompleted.connect(self.on_process_completed)

        # Iniciar el procesamiento en segundo plano
        self.progress_bar.setValue(0)
        self.worker.start()

    def update_progress(self, value):
        """
        Actualizar la barra de progreso en la barra de estado.
        """
        self.progress_bar.setValue(value)

    def on_process_completed(self):
        """
        Acción a realizar cuando el procesamiento se completa.
        """
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Éxito", "El procesamiento se completó con éxito.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
