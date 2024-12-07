import os
from services.ocr_service import OCRHandler
from utils.validation_utils import is_weekly_file

class FileProcessor:
    def __init__(self):
        self.ocr_handler = OCRHandler()

    def process_files_in_folder(self, folder_path, year, month):
        """Procesar archivos en la carpeta."""
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(file_path):
                continue

            if file_name.endswith(("EDD", "941")) or is_weekly_file(file_name, year):
                print(f"Procesando archivo: {file_path}")

                # Verificar si el archivo es editable
                if not self.ocr_handler.is_editable(file_path):
                    print(f"El archivo no es editable, aplicando OCR: {file_path}")
                    self.ocr_handler.apply_ocr(file_path)
