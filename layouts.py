from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox
from widgets import create_button
from excel_processor import insert_balance_formulas
from file_processing import process_excel_and_folders

def create_main_layout(parent):
    """
    Crea y organiza el layout principal.
    :param parent: Referencia a la ventana principal.
    :return: QVBoxLayout
    """
    layout = QVBoxLayout()

    # Botón 1: Seleccionar Excel y procesar carpetas
    button_process = create_button(
        "Seleccionar Excel y Procesar Carpeta",
        lambda: process_excel_and_folders(parent)
    )
    layout.addWidget(button_process)

    # Botón 2: Cruce de montos
    button_cross = create_button(
        "Cruce de Montos",
        lambda: insert_balance_formulas(parent)
    )
    layout.addWidget(button_cross)

    return layout
