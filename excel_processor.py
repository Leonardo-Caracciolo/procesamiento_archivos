import pandas as pd
from exceptions import ExcelProcessingError
from PyQt5.QtWidgets import QFileDialog

def process_excel(file_path):
    """
    Procesa un archivo Excel, manejando errores de formato y conexión.
    """
    if not file_path:
        print("No se seleccionó ningún archivo.")
        return

    try:
        df = pd.read_excel(file_path)

        # Verificar columnas requeridas
        required_columns = ["Company", "Check Date", "Federal Tax", "State Tax", "Payment Date", "941", "EDD"]
        if not all(col in df.columns for col in required_columns):
            raise ExcelProcessingError("El archivo Excel no tiene las columnas requeridas.")

        print("Archivo Excel procesado correctamente.")
        print(df.head())

    except ExcelProcessingError as e:
        print(f"Error al procesar el Excel: {e}")
    except Exception as e:
        print(f"Error inesperado al procesar el Excel: {e}")


from openpyxl import load_workbook

def insert_balance_formulas(parent):
    """
    Inserta fórmulas en las columnas Balance 941 y Balance EDD del archivo Excel.
    """
    try:
        excel_path, _ = QFileDialog.getOpenFileName(parent, "Seleccionar archivo Excel", "", "Excel Files (*.xlsx)")
        if not excel_path:
            print("No se seleccionó ningún archivo.")
            return

        wb = load_workbook(excel_path)
        ws = wb.active

        for row in range(2, ws.max_row + 1):
            ws[f"H{row}"] = f"=C{row}-F{row}"  # Fórmula para Balance 941
            ws[f"I{row}"] = f"=D{row}-G{row}"  # Fórmula para Balance EDD

        wb.save(excel_path)
        print("Fórmulas ingresadas exitosamente.")
    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")
