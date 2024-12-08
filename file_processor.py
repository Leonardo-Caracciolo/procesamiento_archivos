import os
import re
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from services.ocr_service import is_editable, apply_ocr


def process_excel_and_folders(parent):
    """
    Selecciona un Excel, procesa carpetas basándose en la columna Payment Date,
    y actualiza el Excel con datos extraídos.
    """
    # Seleccionar archivo Excel
    excel_path, _ = QFileDialog.getOpenFileName(parent, "Seleccionar archivo Excel", "", "Excel Files (*.xlsx *.xls)")
    if not excel_path:
        QMessageBox.warning(parent, "Error", "No se seleccionó ningún archivo Excel.")
        return

    # Cargar el Excel
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Error al leer el archivo Excel: {e}")
        return

    # Verificar columnas requeridas
    required_columns = ['Company', 'Check Date', 'Federal Tax', 'State Tax', 'Payment Date', '941', 'EDD']
    if not all(col in df.columns for col in required_columns):
        QMessageBox.critical(parent, "Error", "El Excel no contiene las columnas requeridas.")
        return

    # Seleccionar carpeta principal
    parent_folder = QFileDialog.getExistingDirectory(parent, "Seleccionar carpeta principal")
    if not parent_folder:
        QMessageBox.warning(parent, "Error", "No se seleccionó ninguna carpeta.")
        return

    # Procesar carpetas y extraer datos
    for payment_date in df['Payment Date']:
        folder_name = str(payment_date.date())
        folder_path = os.path.join(parent_folder, folder_name)

        if os.path.exists(folder_path):
            process_folder(folder_path, df, payment_date)

    # Guardar cambios en el Excel
    try:
        df.to_excel(excel_path, index=False)
        QMessageBox.information(parent, "Éxito", "Datos procesados y guardados en el Excel.")
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Error al guardar el Excel: {e}")


def process_folder(folder_path, df, payment_date):
    """
    Procesar archivos dentro de una carpeta específica.
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            process_file(file_path, payment_date, df)


def process_file(file_path, payment_date, df):
    """
    Procesar un archivo específico.
    """
    # Validar nombres de archivo
    file_name = os.path.basename(file_path)
    if not (file_name.endswith("EDD") or file_name.endswith("941") or is_weekly_file(file_name, payment_date.year)):
        return

    print(f"Procesando archivo: {file_path}")

    # Verificar si el archivo es editable
    if not is_editable(file_path):
        print(f"El archivo no es editable, aplicando OCR: {file_path}")
        apply_ocr(file_path)

    # Extraer datos del archivo
    extract_data_from_file(file_path, df, payment_date)


def extract_data_from_file(file_path, df, payment_date):
    """
    Extraer información de un archivo utilizando expresiones regulares.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            match = re.search(r'Referencia: (\d+)', content)
            if match:
                df.loc[df['Payment Date'] == payment_date, 'Referencia'] = match.group(1)
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")


def is_weekly_file(file_name, year):
    """
    Verificar si un archivo tiene formato de semana.
    """
    try:
        base_name = file_name.split(".")[0]
        if len(base_name) == 8:
            day, month, file_year = int(base_name[:2]), int(base_name[2:4]), int(base_name[4:])
            return 1 <= day <= 31 and 1 <= month <= 12 and file_year == int(year)
    except ValueError:
        pass
    return False
