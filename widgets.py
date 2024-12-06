from PyQt5.QtWidgets import QPushButton
from styles import BUTTON_STYLE

def create_button(text, function=None, style=None):
    """
    Crea un botón personalizado.
    :param text: Texto que aparecerá en el botón.
    :param function: Función que se ejecutará al hacer clic en el botón.
    :param style: CSS para personalizar el botón.
    :return: QPushButton
    """
    button = QPushButton(text)
    button = QPushButton("Clic aquí")
    button.setStyleSheet(BUTTON_STYLE)
    
    # Conectar función al clic
    if function:
        button.clicked.connect(function)
    
    # Aplicar estilo CSS
    if style:
        button.setStyleSheet(style)
    
    return button
