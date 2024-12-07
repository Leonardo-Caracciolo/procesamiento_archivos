import os
from ocr_handler import is_editable, apply_ocr

def process_file(file_path, year, month):
    """Procesar un archivo específico."""
    if not os.path.isfile(file_path):
        return

    # Validar nombres de archivo
    file_name = os.path.basename(file_path)
    if not (file_name.endswith("EDD") or file_name.endswith("941") or is_weekly_file(file_name, year)):
        return

    print(f"Procesando archivo: {file_path}")

    # Verificar si el archivo es editable
    if not is_editable(file_path):
        print(f"El archivo no es editable, aplicando OCR: {file_path}")
        apply_ocr(file_path)

def is_weekly_file(file_name, year):
    """Verificar si un archivo tiene formato de semana."""
    try:
        base_name = file_name.split(".")[0]
        if len(base_name) == 8:
            day, month, file_year = int(base_name[:2]), int(base_name[2:4]), int(base_name[4:])
            return 1 <= day <= 31 and 1 <= month <= 12 and file_year == int(year)
    except ValueError:
        pass
    return False
