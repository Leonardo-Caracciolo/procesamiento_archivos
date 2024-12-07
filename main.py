import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from mainwindow import Ui_MainWindow  # Importa la interfaz generada

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables para almacenar la carpeta, año y mes seleccionados
        self.selected_folder = ""
        self.selected_year = ""
        self.selected_month = ""

        # Conectar botones a funciones
        self.ui.pushButton.clicked.connect(self.select_folder)
        self.ui.pushButton_2.clicked.connect(self.start_process)

        # Tamaño fijo de la ventana
        self.setFixedSize(300, 300)

    def select_folder(self):
        """Abre un cuadro de diálogo para seleccionar la carpeta."""
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.selected_folder = folder
            print(f"Carpeta seleccionada: {folder}")

    def start_process(self):
        """Lógica para procesar el año y mes seleccionados."""
        self.selected_year = self.ui.yearComboBox.currentText()
        self.selected_month = self.ui.comboBox.currentText()

        # Validar selecciones
        if self.selected_year == "Seleccionar Año" and self.selected_month == "Seleccionar mes":
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un año y un mes válidos.")
        elif self.selected_year == "Seleccionar Año":
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un año válido.")
        elif self.selected_month == "Seleccionar mes":
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un mes válido.")
        elif not self.selected_folder:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una carpeta primero.")
        else:
            # Procesar la información seleccionada
            result = f"Carpeta: {self.selected_folder}\nAño: {self.selected_year}\nMes: {self.selected_month}"
            print(result)
            QMessageBox.information(self, "Información Seleccionada", result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
