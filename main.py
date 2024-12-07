import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from mainwindow import Ui_MainWindow
from services.folder_service import FolderProcessor
from utils.app_logger import setup_logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configuración inicial
        setup_logging()
        self.folder_processor = FolderProcessor()  # Inyección de dependencia
        self.selected_folder = ""
        self.selected_year = ""
        self.selected_month = ""

        # Conectar botones
        self.ui.pushButton.clicked.connect(self.select_folder)
        self.ui.pushButton_2.clicked.connect(self.start_process)
        self.setFixedSize(300, 300)

    def select_folder(self):
        """Permitir al usuario seleccionar la carpeta padre."""
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta Padre")
        if folder:
            self.selected_folder = folder
            print(f"Carpeta seleccionada: {folder}")

    def start_process(self):
        """Iniciar el procesamiento."""
        self.selected_year = self.ui.yearComboBox.currentText()
        self.selected_month = self.ui.comboBox.currentText()

        # Validaciones iniciales
        if self.selected_year == "Seleccionar Año" or self.selected_month == "Seleccionar mes":
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un año y un mes válidos.")
            return
        if not self.selected_folder:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una carpeta primero.")
            return

        # Procesar carpetas
        try:
            self.folder_processor.process(self.selected_folder, self.selected_year, self.selected_month)
            QMessageBox.information(self, "Éxito", "El proceso se completó correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
