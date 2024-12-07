class FolderNotFoundError(Exception):
    """Excepción para carpetas no encontradas."""
    pass

class InvalidYearOrMonthError(Exception):
    """Excepción para valores de año o mes no válidos."""
    def __init__(self, year, month):
        self.year = year
        self.month = month
        super().__init__(f"Valores inválidos: Año={year}, Mes={month}")

class FileProcessingError(Exception):
    """Excepción genérica para errores al procesar archivos."""
    pass

class OCRNotInstalledError(Exception):
    """Excepción cuando Tesseract OCR no está instalado."""
    def __init__(self):
        super().__init__("Tesseract OCR no está instalado. Por favor, instálalo para continuar.")
