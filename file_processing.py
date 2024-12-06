import os
import re
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox

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
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        match = re.search(r'Referencia: (\d+)', content)
                        if match:
                            df.loc[df['Payment Date'] == payment_date, 'Referencia'] = match.group(1)

    # Guardar cambios en el Excel
    try:
        df.to_excel(excel_path, index=False)
        QMessageBox.information(parent, "Éxito", "Datos procesados y guardados en el Excel.")
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Error al guardar el Excel: {e}")
