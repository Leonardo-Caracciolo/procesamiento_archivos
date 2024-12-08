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
        """
        Opens a dialog box for selecting the parent folder.

        This method displays a file dialog that allows the user to choose
        a directory. If a directory is selected, it updates the
        `selected_folder` attribute of the class and prints the selected
        folder path.

        Returns:
            None
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

        # Procesar carpetas
        folder_processor = FolderProcessor()
        folder_processor.process(self.selected_folder, self.selected_year, self.selected_month)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
