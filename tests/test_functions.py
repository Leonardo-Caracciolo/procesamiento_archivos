import os
import pandas as pd

# def process_weekly_files(folder_path, year, month, total_files, processed_files):
#     columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd',
#                     '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle', 'carpeta_cliente']
#     df = pd.DataFrame(columns=columnas)
#     carpeta_cliente = os.path.basename(os.path.dirname(os.path.dirname(folder_path)))
#     print(carpeta_cliente)

#     week_read = None
#     for file_name in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, file_name)
#         df_no_files = pd.DataFrame()

#         if not os.path.isfile(file_path):
#             continue

#         if not any(file_name.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"]):
#             continue
        
#         # Validamos si hay archivos faltantes para la semana que estamos recorriendo
        
#         week = file_name[:8]
#         look_files = (f"{week} EDD.pdf", f"{week} 941.pdf", f"{week}.pdf")
#         if week_read != week:
#             for file in look_files: # Ruta completa del archivo file_path = os.path.join(folder_path, file_name)
#                 file_possible_path = os.path.join(folder_path, file)
#                 if not os.path.isfile(file_possible_path): 
#                     print(f"El archivo {file} no existe.")
#                     df_no_files = pd.DataFrame([{
#                         'tipo_archivo': "941",
#                         'fecha_pdf': week,
#                         'carpeta_cliente': carpeta_cliente,
#                         'ruta_archivo' : "Archivo no encontrado"
#                     }])
#                     week_read = week

#         print(f"Procesando archivo: {os.path.abspath(file_path)}")

#         text = self.process_file_with_ocr(file_path)
#         datos = self.handle_extracted_data(file_name, text, carpeta_cliente, month, year)

#         df = pd.concat([df, datos], ignore_index=True)

#         # Actualizar el progreso y emitir la señal
#         self.processed_files += 1
#         progress = int((self.processed_files / total_files) * 100)
#         self.progressChanged.emit(progress)

#     df = pd.concat([df, df_no_files], ignore_index=True)
#     return df

from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

def validation_data(path_file):
    """
    Indicamos resaltando con un color que archivos no fueron encontrados en sus carpetas
    """
    # Seleccionar archivo Excel
    excel_path = path_file

    # Abrir el archivo Excel con openpyxl
    try:
        wb = load_workbook(excel_path)
        ws = wb['Datos combinados']

        # Definir el color de fondo (amarillo)
        color_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        # Insertar fórmulas en las columnas H y I
        for row in range(2, ws.max_row + 1):  # Asume que la fila 1 es el encabezado
            if ws[f"K{row}"].value == "Archivo no encontrado":
                for col in range(1, 12): # Recorrer todas las celdas en la fila
                    cell = ws.cell(row=row, column=col)
                    cell.fill = color_fill

        # Guardar cambios
        wb.save(excel_path)
        print("Excel modificado con exito.")
    except Exception as e:
        print("Error al cargar la formula")

if __name__ == "__main__":

    # folder_path = r"C:\Users\seba\Desktop\Proyectos\Repo_Leo\procesamiento_archivos\Data\Inputs\Inputs-2\Clientes_faltantes_lectura\D02-DSL FINISHING\12- December"
    # year = 2024
    # month = 12
    # total_files = 100 
    # processed_files = ""

    # df = process_weekly_files(folder_path, year, month, total_files, processed_files)
    # print(df.head())
    path_excel = r"C:\Users\seba\Desktop\Proyectos\Repo_Leo\procesamiento_archivos\services\carpeta_clientes_unificados\datos_combinados.xlsx"
    validation_data(path_excel)