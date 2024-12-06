from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from layouts import create_main_layout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("Procesador de PDFs y Excel")
        self.setGeometry(100, 100, 1000, 600)

        # Crear un widget contenedor para el layout
        central_widget = QWidget()
        central_layout = create_main_layout(self)  # Obtiene el layout
        central_widget.setLayout(central_layout)  # Asigna el layout al widget

        # Establecer el widget contenedor como central
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error crítico: {e}")
