import os
from services.file_service import FileProcessor
from utils.validation_utils import validate_year_month

class FolderProcessor:
    def __init__(self):
        self.file_processor = FileProcessor()

    def process(self, parent_folder, year, month):
        """Procesar carpetas de clientes."""
        validate_year_month(year, month)  # Validación de datos de entrada
        payroll_folder_name = f"Payroll {year}"
        year_folder_name = f"{year}"

        for client_folder in os.listdir(parent_folder):
            client_path = os.path.join(parent_folder, client_folder)

            if not os.path.isdir(client_path):
                continue

            target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name)
            if not target_path:
                print(f"No se encontró carpeta válida en: {client_path}")
                continue

            print(f"Procesando carpeta: {target_path}")
            self.file_processor.process_files_in_folder(target_path, year, month)

    def _get_target_path(self, client_path, payroll_folder_name, year_folder_name):
        """Buscar carpeta objetivo dentro del cliente."""
        payroll_path = os.path.join(client_path, payroll_folder_name)
        year_path = os.path.join(client_path, year_folder_name)

        if os.path.exists(payroll_path):
            return payroll_path
        if os.path.exists(year_path):
            return year_path
        return None
