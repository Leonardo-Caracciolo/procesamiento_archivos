import os

def install_tesseract():
    """Instala Tesseract OCR si no está presente."""
    try:
        if os.name == "nt":  # Windows
            os.system("choco install tesseract")
        else:  # Linux/Mac
            os.system("sudo apt-get install tesseract-ocr")
        print("Tesseract OCR instalado correctamente.")
    except Exception as e:
        print(f"Error al intentar instalar Tesseract OCR: {e}")
