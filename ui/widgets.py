from PyQt5.QtWidgets import QPushButton
from ui.styles import BUTTON_STYLE  # Ajusta la ruta según tu estructura

def create_button(text, function=None, style=None):
    """
    Crea un botón personalizado.
    :param text: Texto que aparecerá en el botón.
    :param function: Función que se ejecutará al hacer clic en el botón.
    :param style: CSS para personalizar el botón.
    :return: QPushButton
    """
    # Crear el botón con el texto proporcionado
    button = QPushButton(text)
    
    # Aplicar estilo CSS (por defecto o personalizado)
    if style:
        button.setStyleSheet(style)
    else:
        button.setStyleSheet(BUTTON_STYLE)

    # Conectar la función al clic, si se proporciona
    if function:
        button.clicked.connect(function)
    
    return button
