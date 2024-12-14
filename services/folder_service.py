# import os
# import pytesseract
# import fitz  # PyMuPDF para trabajar con PDFs
# from PIL import Image
# import pandas as pd
# import numpy as np
# import services.func_extrac_data as look_data  # Asegúrate de que esta ruta sea correcta
# from openpyxl import load_workbook
# from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# from PyQt5.QtCore import QObject, pyqtSignal, QThread

# # Diccionario para traducir meses entre inglés y español


# class FolderProcessor(QObject):
#     progressChanged = pyqtSignal(int)

#     def __init__(self, output_folder, output_file):
#         super().__init__()  # Llamar al constructor de QObject
#         self.output_folder = output_folder  # Carpeta donde se guardarán los archivos
#         self.output_file = output_file  # Archivo Excel final
#         os.makedirs(output_folder, exist_ok=True)  # Crear carpeta de salida si no existe

#     def process(self, parent_folder, year, month):
#         payroll_folder_name = f"Payroll {year}"
#         year_folder_name = str(year)
#         translated_month = self.translate_month(month)  # Traduce el mes al idioma necesario

#         combined_df = pd.DataFrame()

#         client_folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
#         total_folders = len(client_folders)
#         total_files = 0
#         self.processed_files = 0

#         # Contar todos los archivos que se van a procesar
#         for client_folder in client_folders:
#             client_path = os.path.join(parent_folder, client_folder)
#             target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name, translated_month)
#             if not target_path:
#                 continue
#             total_files += len([f for f in os.listdir(target_path) if any(f.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"])])

#         for client_folder in client_folders:
#             client_path = os.path.join(parent_folder, client_folder)
#             target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name, translated_month)
#             if not target_path:
#                 print(f"No se encontró carpeta válida en: {os.path.abspath(client_path)}")
#                 continue

#             print(f"Procesando carpeta: {os.path.abspath(target_path)}")
#             df_weekly = self.process_weekly_files(target_path, year, translated_month, total_files, self.processed_files)
#             combined_df = pd.concat([combined_df, df_weekly], ignore_index=True)

#         df_modify = self.prepare_data(combined_df)
#         # Guardar todos los datos combinados en un solo archivo Excel
#         self.save_to_excel(os.path.join(self.output_folder, self.output_file), df_modify)

#     def clean_path_segment(self, segment):
#         # Reemplazar espacios en "mes-numero" para que quede "numero_mes+mes"
#         return segment.replace(" ", "")

#     def _get_target_path(self, client_path, payroll_folder_name, year_folder_name, month):
#         month_number = self.get_month_number(month)
#         possible_paths = [
#             os.path.join(client_path, payroll_folder_name, self.clean_path_segment(f"{month_number} - {month}")),
#             os.path.join(client_path, year_folder_name, self.clean_path_segment(f"{month_number} - {month}")),
#             os.path.join(client_path, payroll_folder_name, month),
#             os.path.join(client_path, year_folder_name, month),
#             os.path.join(client_path, f"{year_folder_name} - {month}")
#         ]
#         print(f"posbile:{os.path.abspath(client_path)}")

#         for path in possible_paths:

#             if os.path.exists(path):
#                 return path
#         return None


#     def process_weekly_files(self, folder_path, year, month, total_files, processed_files):
#         columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd',
#                     '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle', 'carpeta_cliente']
#         df = pd.DataFrame(columns=columnas)
#         carpeta_cliente = os.path.basename(os.path.dirname(os.path.dirname(folder_path)))
#         print(carpeta_cliente)
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)

#             if not os.path.isfile(file_path):
#                 continue

#             if not any(file_name.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"]):
#                 continue

#             print(f"Procesando archivo: {os.path.abspath(file_path)}")
#             text = self.process_file_with_ocr(file_path)
#             datos = self.handle_extracted_data(file_name, text, carpeta_cliente, month, year)

#             df = pd.concat([df, datos], ignore_index=True)

#             # Actualizar el progreso y emitir la señal
#             self.processed_files += 1
#             progress = int((self.processed_files / total_files) * 100)
#             self.progressChanged.emit(progress)

#         return df


#     def process_file_with_ocr(self, file_path):
#         try:
#             pdf_document = fitz.open(file_path)
#             extracted_text = ""
#             last_page_number = len(pdf_document) - 1
#             page = pdf_document[last_page_number]
#             pix = page.get_pixmap(dpi=600)
#             image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             extracted_text += pytesseract.image_to_string(image, lang='spa', config='--dpi 600')
#             return extracted_text
#         except Exception as e:
#             print(f"Error al procesar el archivo con OCR: {e}")
#             return ""

#     def handle_extracted_data(self, file_name, text, carpeta_cliente, month, year):
#         def format_date(date_str):
#             try:
#                 return pd.to_datetime(date_str).strftime('%Y-%m-%d')
#             except ValueError:
#                 return date_str

#         if file_name.endswith("941.pdf"):
#             return pd.DataFrame([{
#                 'tipo_archivo': "941",
#                 'fecha_pdf': file_name.replace('941.pdf', ''),
#                 'Name': look_data.extract_payer_name(text),
#                 '941_payment_amount': look_data.extract_payment_amount_941(text),
#                 'account_number': look_data.extract_account_number(text),
#                 'date_pay_settle': format_date(look_data.extract_settlement_date(text)),
#                 'carpeta_cliente': carpeta_cliente
#             }])
#         elif file_name.endswith("EDD.pdf"):
#             return pd.DataFrame([{
#                 'tipo_archivo': "EDD",
#                 'fecha_pdf': file_name.replace('EDD.pdf', ''),
#                 'Name': look_data.extract_name(text),
#                 'EDD_payment_amount': look_data.extract_payment_amount_edd(text, 2),
#                 'account_number': look_data.extract_account_number(text),
#                 'date_pay_settle': format_date(look_data.extract_payment_date(text)),
#                 'carpeta_cliente': carpeta_cliente
#             }])
#         else:
#             return pd.DataFrame([{
#                 'tipo_archivo': "general",
#                 'fecha_pdf': file_name.replace('.pdf', ''),
#                 'Name': look_data.extract_company_name(text),
#                 'federal_tax_941': look_data.extract_payment_amount_general_941(text),
#                 'state_tax_edd': look_data.extract_payment_amount_general_edd(text),
#                 'carpeta_cliente': carpeta_cliente
#             }])

#     def group_by_weekly(self, dataframe):
#         """
#         Agrupa los datos por carpeta_cliente y fecha_pdf para consolidar información.
#         """

#         dataframe['Check date'] = dataframe['Check date'].astype(int)
#         # Obtener combinaciones únicas de 'carpeta_cliente' y 'fecha_pdf'
#         combinaciones_unicas = dataframe[['Company', 'Check date']].drop_duplicates()

#         resultados = []

#         for _, fila in combinaciones_unicas.iterrows():
#             carpeta_cliente = fila['Company']
#             fecha = fila['Check date']
#             df_filtrado = dataframe[(dataframe['Company'] == carpeta_cliente) & (dataframe['Check date'] == fecha)]
#             resultado = {'Company': carpeta_cliente, 'Check date': fecha}

#             for columna in ['Federal Tax', 'State Tax', 'Payment date' ,'941', 'EDD']:
#                 valores = df_filtrado[columna].replace('', np.nan).dropna()
#                 resultado[columna] = valores.iloc[0] if not valores.empty else np.nan

#             resultados.append(resultado)

#         return pd.DataFrame(resultados)

#     def format_excel_headers(self, file_path, headers):
#         """
#         Formatea los encabezados de un archivo Excel con las especificaciones proporcionadas.

#         :param file_path: Ruta al archivo Excel.
#         :param headers: Lista de encabezados que se esperan en la primera fila.
#         """
#         try:
#             # Cargar el archivo Excel
#             wb = load_workbook(file_path)
#             ws = wb["Resumen"]

#             # Configuración de estilo
#             header_style = {
#                 "font": Font(name="Calibri", size=20, bold=False, color="000000"),
#                 "fill": PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"),
#                 "alignment": Alignment(horizontal="center", vertical="center"),
#                 "border": Border(
#                     left=Side(style="thin"),
#                     right=Side(style="thin"),
#                     top=Side(style="thin"),
#                     bottom=Side(style="thin")
#                 )
#             }

#             # Aplicar formato a los encabezados
#             for col, header in enumerate(headers, start=1):
#                 cell = ws.cell(row=1, column=col, value=header)
#                 for attr, value in header_style.items():
#                     setattr(cell, attr, value)

#             # Ajustar automáticamente el ancho de las columnas
#             for col in ws.columns:
#                 max_length = 0
#                 column = col[0].column_letter  # Obtiene la letra de la columna
#                 for cell in col:
#                     try:
#                         if cell.value:
#                             max_length = max(max_length, len(str(cell.value)))
#                     except:
#                         pass
#                 adjusted_width = (max_length + 2)
#                 ws.column_dimensions[column].width = adjusted_width

#             # Guardar los cambios en el archivo
#             wb.save(file_path)
#             print(f"Encabezados formateados correctamente en el archivo: {file_path}")

#         except Exception as e:
#             print(f"Error al formatear los encabezados: {e}")


#     def crossamounts(self, path_file):
#         """
#         Inserta fórmulas en las columnas Balance 941 y Balance EDD.
#         """
#         # Seleccionar archivo Excel
#         excel_path = path_file

#         # Abrir el archivo Excel con openpyxl
#         try:
#             wb = load_workbook(excel_path)
#             ws = wb['Resumen']

#             ws.cell(1,8).value = 'Balance 941'
#             ws.cell(1,9).value = 'Balance EDD'

#             # Insertar fórmulas en las columnas H y I
#             for row in range(2, ws.max_row + 1):  # Asume que la fila 1 es el encabezado
#                 ws[f"H{row}"] = f"=C{row}-F{row}"  # Balance 941
#                 ws[f"I{row}"] = f"=D{row}-G{row}"  # Balance EDD

#             # Guardar cambios
#             wb.save(excel_path)
#             print("Fórmulas ingresadas en el archivo Excel.")
#         except Exception as e:
#             print("Error al cargar la formula")


#     def prepare_data(self, df):

#         df = pd.DataFrame(df)

#         df['federal_tax_941'] = df['federal_tax_941'].str.replace(',', '')
#         df['federal_tax_941'] = df['federal_tax_941'].str.replace('.', ',')

#         df['state_tax_edd'] = df['state_tax_edd'].str.replace(',', '')
#         df['state_tax_edd'] = df['state_tax_edd'].str.replace('.', ',')

#         df['941_payment_amount'] = df['941_payment_amount'].str.replace(',', '')
#         df['941_payment_amount'] = df['941_payment_amount'].str.replace('.', ',')

#         df['EDD_payment_amount'] = df['EDD_payment_amount'].str.replace(',', '')
#         df['EDD_payment_amount'] = df['EDD_payment_amount'].str.replace('.', ',')


#         df = df.rename(columns={
#             'carpeta_cliente': 'Company',
#             'fecha_pdf': 'Check date',
#             'federal_tax_941': 'Federal Tax',
#             'state_tax_edd': 'State Tax',
#             'date_pay_settle': 'Payment date',
#             '941_payment_amount': '941',
#             'EDD_payment_amount':'EDD'
#             })

#         return df


#     def save_to_excel(self, file_path, df_new):

#         try:
#             # Escribir el DataFrame en una nueva hoja
#             df_resultado = self.group_by_weekly(df_new)

#             # df_resultado.to_excel(ruta1, index=False, sheet_name="Resumen")
#             with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
#                 df_resultado.to_excel(writer, index=False, sheet_name='Resumen')
#                 df_new.to_excel(writer, index=False, sheet_name='Datos combinados')

#             print(f"Datos guardados en la hoja Datos combinados del archivo {file_path}")
#             print(f"Datos guardados en la hoja Datos combinados del archivo {file_path}")

#         except Exception as e:
#             print(f"Error al guardar los datos en el archivo Excel: {e}")

#         self.crossamounts(file_path)
#         headers = ["Company","Check date","Federal Tax","State Tax","Payment date","941",'EDD', 'Balance 941', 'Balance EDD']
#         self.format_excel_headers(file_path, headers)

#     def translate_month(self, month):
#         return months_translator.get(month, month)

#---------------------------------funcionan los test (4)
# import os
# import pytesseract
# import fitz  # PyMuPDF para trabajar con PDFs
# from PIL import Image
# import pandas as pd
# import numpy as np
# from openpyxl import load_workbook
# from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
# from PyQt5.QtCore import QObject, pyqtSignal
# import logging
# import json
# from concurrent.futures import ThreadPoolExecutor
# from datetime import datetime
# import services.func_extrac_data as look_data

# # Configuración del logger
# logging.basicConfig(
#     filename="process.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# months_translator = {
#     "January": "Enero",
#     "February": "Febrero",
#     "March": "Marzo",
#     "April": "Abril",
#     "May": "Mayo",
#     "June": "Junio",
#     "July": "Julio",
#     "August": "Agosto",
#     "September": "Septiembre",
#     "October": "Octubre",
#     "November": "Noviembre",
#     "December": "Diciembre",
#     "Enero": "January",
#     "Febrero": "February",
#     "Marzo": "March",
#     "Abril": "April",
#     "Mayo": "May",
#     "Junio": "June",
#     "Julio": "July",
#     "Agosto": "August",
#     "Septiembre": "September",
#     "Octubre": "October",
#     "Noviembre": "November",
#     "Diciembre": "December",
# }

# months_numbers = {
#     "January": 1,
#     "February": 2,
#     "March": 3,
#     "April": 4,
#     "May": 5,
#     "June": 6,
#     "July": 7,
#     "August": 8,
#     "September": 9,
#     "October": 10,
#     "November": 11,
#     "December": 12,
#     "Enero": 1,
#     "Febrero": 2,
#     "Marzo": 3,
#     "Abril": 4,
#     "Mayo": 5,
#     "Junio": 6,
#     "Julio": 7,
#     "Agosto": 8,
#     "Septiembre": 9,
#     "Octubre": 10,
#     "Noviembre": 11,
#     "Diciembre": 12,
# }


# class ErrorLogger:
#     """
#     Clase para gestionar errores durante el proceso.
#     """

#     def __init__(self, log_path):
#         self.log_path = log_path
#         self.errors = []

#     def log_error(self, file_name, error_message):
#         """
#         Registra un error en el log.
#         :param file_name: Nombre del archivo donde ocurrió el error.
#         :param error_message: Mensaje del error.
#         """
#         self.errors.append({"file": file_name, "error": error_message})
#         logging.error(f"Error en {file_name}: {error_message}")

#     def save_log(self):
#         """
#         Guarda el log de errores en un archivo JSON.
#         """
#         with open(self.log_path, "w") as log_file:
#             json.dump(self.errors, log_file, indent=4)


# class FolderProcessor(QObject):
#     """
#     Clase para procesar carpetas de clientes y generar un reporte consolidado en Excel.
#     """

#     progressChanged = pyqtSignal(int)

#     def __init__(self, output_folder, output_file):
#         """
#         Inicializa el procesador de carpetas.
#         :param output_folder: Carpeta donde se guardará el archivo de salida.
#         :param output_file: Nombre del archivo Excel de salida.
#         """
#         super().__init__()
#         self.output_folder = output_folder
#         self.output_file = output_file
#         os.makedirs(output_folder, exist_ok=True)
#         self.processed_files = 0
#         self.failed_files = []
#         self.failed_weeks = []
#         self.error_logger = ErrorLogger(os.path.join(output_folder, "error_log.json"))

#     def _get_target_path(
#         self, client_path, payroll_folder_name, year_folder_name, month
#     ):
#         month_number = self.get_month_number(month)
#         possible_paths = [
#             os.path.join(
#                 client_path,
#                 payroll_folder_name,
#                 self.clean_path_segment(f"{month_number} - {month}"),
#             ),
#             os.path.join(
#                 client_path,
#                 year_folder_name,
#                 self.clean_path_segment(f"{month_number} - {month}"),
#             ),
#             os.path.join(client_path, payroll_folder_name, month),
#             os.path.join(client_path, year_folder_name, month),
#             os.path.join(client_path, f"{year_folder_name} - {month}"),
#         ]
#         print(f"posbile:{os.path.abspath(client_path)}")

#         for path in possible_paths:

#             if os.path.exists(path):
#                 return path
#         return None

#     def validate_inputs(self, parent_folder, year, month):
#         """
#         Valida los parámetros de entrada.
#         """
#         if not os.path.isdir(parent_folder):
#             raise FileNotFoundError(
#                 f"La carpeta {parent_folder} no existe o no es accesible."
#             )
#         if not isinstance(year, int) or year < 2000 or year > 2100:
#             raise ValueError("El año debe ser un valor entre 2000 y 2100.")
#         if (
#             month not in months_translator.keys()
#             and month not in months_translator.values()
#         ):
#             raise ValueError(f"El mes {month} no es válido.")

#     def process_file_with_ocr(self, file_path):
#         """
#         Procesa un archivo PDF con OCR para extraer texto.
#         """
#         try:
#             pdf_document = fitz.open(file_path)
#             last_page = pdf_document[-1]
#             pix = last_page.get_pixmap(dpi=600)
#             image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             return pytesseract.image_to_string(image, lang="spa", config="--dpi 600")
#         except Exception as e:
#             self.error_logger.log_error(file_path, f"OCR Error: {str(e)}")
#             raise RuntimeError(f"Error procesando OCR en {file_path}: {e}")

#     def handle_extracted_data(self, file_name, text, carpeta_cliente, month, year):
#         def format_date(date_str):
#             try:
#                 return pd.to_datetime(date_str).strftime("%Y-%m-%d")
#             except ValueError:
#                 return date_str

#         try:
#             if file_name.endswith("941.pdf"):
#                 return pd.DataFrame(
#                     [
#                         {
#                             "tipo_archivo": "941",
#                             "fecha_pdf": file_name.replace("941.pdf", ""),
#                             "Name": look_data.extract_payer_name(text),
#                             "941_payment_amount": look_data.extract_payment_amount_941(
#                                 text
#                             ),
#                             "account_number": look_data.extract_account_number(text),
#                             "date_pay_settle": self.format_date(
#                                 look_data.extract_settlement_date(text)
#                             ),
#                             "carpeta_cliente": carpeta_cliente,
#                         }
#                     ]
#                 )
#             elif file_name.endswith("EDD.pdf"):
#                 return pd.DataFrame(
#                     [
#                         {
#                             "tipo_archivo": "EDD",
#                             "fecha_pdf": file_name.replace("EDD.pdf", ""),
#                             "Name": look_data.extract_name(text),
#                             "EDD_payment_amount": look_data.extract_payment_amount_edd(
#                                 text
#                             ),
#                             "account_number": look_data.extract_account_number(text),
#                             "date_pay_settle": self.format_date(
#                                 look_data.extract_payment_date(text)
#                             ),
#                             "carpeta_cliente": carpeta_cliente,
#                         }
#                     ]
#                 )
#             else:
#                 return pd.DataFrame()
#         except Exception as e:
#             self.error_logger.log_error(file_name, f"Extraction Error: {str(e)}")
#             raise

#     def process_weekly_files(self, folder_path, year, month, total_files):
#         """
#         Procesa todos los archivos PDF de una carpeta semanal.
#         """
#         columnas = [
#             "tipo_archivo",
#             "fecha_pdf",
#             "Name",
#             "federal_tax_941",
#             "state_tax_edd",
#             "941_payment_amount",
#             "EDD_payment_amount",
#             "account_number",
#             "date_pay_settle",
#             "carpeta_cliente",
#         ]
#         df = pd.DataFrame(columns=columnas)
#         carpeta_cliente = os.path.basename(folder_path)

#     def translate_month(self, month):
#         return months_translator.get(month, month)

#         def process_single_file(file_name):
#             """
#             Procesa un archivo individual y lo convierte en un DataFrame.
#             """
#             file_path = os.path.join(folder_path, file_name)
#             text = self.process_file_with_ocr(file_path)
#             return self.handle_extracted_data(
#                 file_name, text, carpeta_cliente, month, year
#             )

#         # Procesamiento paralelo
#         file_names = [
#             f
#             for f in os.listdir(folder_path)
#             if os.path.isfile(os.path.join(folder_path, f))
#             and any(f.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"])
#         ]

#         with ThreadPoolExecutor(max_workers=4) as executor:
#             try:
#                 results = list(executor.map(process_single_file, file_names))
#                 df = (
#                     pd.concat(results, ignore_index=True) if results else pd.DataFrame()
#                 )
#                 self.processed_files += len(file_names)
#                 progress = int((self.processed_files / total_files) * 100)
#                 self.progressChanged.emit(progress)
#             except Exception as e:
#                 self.failed_weeks.append(carpeta_cliente)
#                 self.error_logger.log_error(
#                     folder_path, f"Weekly Processing Error: {str(e)}"
#                 )
#         return df

#     def get_month_number(self, month):
#         return months_numbers.get(month, "Mes desconocido")

#     def format_excel_headers(self, file_path, headers):
#         """
#         Formatea los encabezados de un archivo Excel con las especificaciones proporcionadas.

#         :param file_path: Ruta al archivo Excel.
#         :param headers: Lista de encabezados que se esperan en la primera fila.
#         """
#         try:
#             # Cargar el archivo Excel
#             wb = load_workbook(file_path)
#             ws = wb["Resumen"]

#             # Configuración de estilo
#             header_style = {
#                 "font": Font(name="Calibri", size=20, bold=False, color="000000"),
#                 "fill": PatternFill(
#                     start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"
#                 ),
#                 "alignment": Alignment(horizontal="center", vertical="center"),
#                 "border": Border(
#                     left=Side(style="thin"),
#                     right=Side(style="thin"),
#                     top=Side(style="thin"),
#                     bottom=Side(style="thin"),
#                 ),
#             }

#             # Aplicar formato a los encabezados
#             for col, header in enumerate(headers, start=1):
#                 cell = ws.cell(row=1, column=col, value=header)
#                 for attr, value in header_style.items():
#                     setattr(cell, attr, value)

#             # Ajustar automáticamente el ancho de las columnas
#             for col in ws.columns:
#                 max_length = 0
#                 column = col[0].column_letter  # Obtiene la letra de la columna
#                 for cell in col:
#                     try:
#                         if cell.value:
#                             max_length = max(max_length, len(str(cell.value)))
#                     except:
#                         pass
#                 adjusted_width = max_length + 2
#                 ws.column_dimensions[column].width = adjusted_width

#             # Guardar los cambios en el archivo
#             wb.save(file_path)
#             print(f"Encabezados formateados correctamente en el archivo: {file_path}")

#         except Exception as e:
#             print(f"Error al formatear los encabezados: {e}")

#     def process(self, parent_folder, year, month):
#         """
#         Procesa todas las carpetas y genera un reporte consolidado.
#         """
#         start_time = datetime.now()
#         try:
#             self.validate_inputs(parent_folder, year, month)
#             payroll_folder_name = f"Payroll {year}"
#             translated_month = self.translate_month(month)
#             combined_df = pd.DataFrame()

#             client_folders = [
#                 f
#                 for f in os.listdir(parent_folder)
#                 if os.path.isdir(os.path.join(parent_folder, f))
#             ]
#             total_files = sum(
#                 len(
#                     [
#                         f
#                         for f in os.listdir(os.path.join(parent_folder, folder))
#                         if any(
#                             f.endswith(suffix + ".pdf")
#                             for suffix in ["EDD", "941", f"{year}"]
#                         )
#                     ]
#                 )
#                 for folder in client_folders
#             )

#             for client_folder in client_folders:
#                 client_path = os.path.join(parent_folder, client_folder)
#                 target_path = self._get_target_path(
#                     client_path, payroll_folder_name, str(year), translated_month
#                 )
#                 if not target_path:
#                     logging.warning(f"Carpeta no válida: {client_path}")
#                     continue
#                 weekly_df = self.process_weekly_files(
#                     target_path, year, translated_month, total_files
#                 )
#                 if not weekly_df.empty:
#                     combined_df = pd.concat([combined_df, weekly_df], ignore_index=True)
#                 else:
#                     self.failed_weeks.append(client_folder)

#             if not combined_df.empty:
#                 # headers = ["Company","Check date","Federal Tax","State Tax","Payment date","941",'EDD', 'Balance 941', 'Balance EDD']
#                 # self.format_excel_headers(file_path, headers)
#                 self.save_to_excel(
#                     os.path.join(self.output_folder, self.output_file), combined_df
#                 )

#         except Exception as e:
#             logging.critical(f"Error crítico: {e}")

#         finally:
#             end_time = datetime.now()
#             self.generate_summary(start_time, end_time)
#             self.error_logger.save_log()

#     def generate_summary(self, start_time, end_time):
#         """
#         Genera un resumen del proceso en un archivo JSON.
#         """
#         summary = {
#             "start_time": str(start_time),
#             "end_time": str(end_time),
#             "total_files_processed": self.processed_files,
#             "failed_files": self.failed_files,
#             "failed_weeks": self.failed_weeks,
#         }
#         summary_path = os.path.join(self.output_folder, "summary.json")
#         with open(summary_path, "w") as summary_file:
#             json.dump(summary, summary_file, indent=4)
#         logging.info(f"Resumen guardado en {summary_path}")
import os
import pytesseract
import fitz  # PyMuPDF para trabajar con PDFs
from PIL import Image
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from PyQt5.QtCore import QObject, pyqtSignal
import logging
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import services.func_extrac_data as look_data

# Configuración del logger
logging.basicConfig(
    filename="process.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

months_translator = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre",
    "Enero": "January",
    "Febrero": "February",
    "Marzo": "March",
    "Abril": "April",
    "Mayo": "May",
    "Junio": "June",
    "Julio": "July",
    "Agosto": "August",
    "Septiembre": "September",
    "Octubre": "October",
    "Noviembre": "November",
    "Diciembre": "December",
}

months_numbers = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12,
}

class ErrorLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.errors = []

    def log_error(self, file_name, error_message):
        self.errors.append({"file": file_name, "error": error_message})
        logging.error(f"Error en {file_name}: {error_message}")

    def save_log(self):
        with open(self.log_path, "w") as log_file:
            json.dump(self.errors, log_file, indent=4)

class FolderProcessor(QObject):
    progressChanged = pyqtSignal(int)

    def __init__(self, output_folder, output_file):
        super().__init__()
        self.output_folder = output_folder
        self.output_file = output_file
        os.makedirs(output_folder, exist_ok=True)
        self.processed_files = 0
        self.failed_files = []
        self.failed_weeks = []
        self.error_logger = ErrorLogger(os.path.join(output_folder, "error_log.json"))

    def validate_inputs(self, parent_folder, year, month):
        if not os.path.isdir(parent_folder):
            raise FileNotFoundError(f"La carpeta {parent_folder} no existe o no es accesible.")
        if not isinstance(year, int) or year < 2000 or year > 2100:
            raise ValueError("El año debe ser un valor entre 2000 y 2100.")
        if month not in months_translator.keys() and month not in months_translator.values():
            raise ValueError(f"El mes {month} no es válido.")

    def translate_month(self, month):
        return months_translator.get(month, month)

    def get_month_number(self, month):
        return months_numbers.get(month, "Mes desconocido")

    def _get_target_path(self, client_path, payroll_folder_name, year_folder_name, month):
        month_number = self.get_month_number(month)
        possible_paths = [
            os.path.join(client_path, payroll_folder_name, f"{month_number} - {month}"),
            os.path.join(client_path, year_folder_name, f"{month_number} - {month}"),
            os.path.join(client_path, payroll_folder_name, month),
            os.path.join(client_path, year_folder_name, month),
            os.path.join(client_path, f"{year_folder_name} - {month}"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def process_file_with_ocr(self, file_path):
        try:
            pdf_document = fitz.open(file_path)
            last_page = pdf_document[-1]
            pix = last_page.get_pixmap(dpi=600)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return pytesseract.image_to_string(image, lang="spa", config="--dpi 600")
        except Exception as e:
            self.error_logger.log_error(file_path, f"OCR Error: {str(e)}")
            raise RuntimeError(f"Error procesando OCR en {file_path}: {e}")

    def format_date(self, date_str):
        try:
            return pd.to_datetime(date_str).strftime("%Y-%m-%d")
        except ValueError:
            return "Fecha inválida"

    def handle_extracted_data(self, file_name, text, carpeta_cliente, month, year):

        try:
            if file_name.endswith("941.pdf"):
                return pd.DataFrame([
                    {
                        "tipo_archivo": "941",
                        "fecha_pdf": file_name.replace("941.pdf", ""),
                        "Name": look_data.extract_payer_name(text),
                        "941_payment_amount": look_data.extract_payment_amount_941(text),
                        "account_number": look_data.extract_account_number(text),
                        "date_pay_settle": self.format_date(look_data.extract_settlement_date(text)),
                        "carpeta_cliente": carpeta_cliente,
                    }
                ])
            elif file_name.endswith("EDD.pdf"):
                return pd.DataFrame([
                    {
                        "tipo_archivo": "EDD",
                        "fecha_pdf": file_name.replace("EDD.pdf", ""),
                        "Name": look_data.extract_name(text),
                        "EDD_payment_amount": look_data.extract_payment_amount_edd(text),
                        "account_number": look_data.extract_account_number(text),
                        "date_pay_settle": self.format_date(look_data.extract_payment_date(text)),
                        "carpeta_cliente": carpeta_cliente,
                    }
                ])
            else:
                return pd.DataFrame()
        except Exception as e:
            self.error_logger.log_error(file_name, f"Extraction Error: {str(e)}")
            raise

    # def process_weekly_files(self, folder_path, year, month, total_files):
    #     columnas = [
    #         "tipo_archivo",
    #         "fecha_pdf",
    #         "Name",
    #         "federal_tax_941",
    #         "state_tax_edd",
    #         "941_payment_amount",
    #         "EDD_payment_amount",
    #         "account_number",
    #         "date_pay_settle",
    #         "carpeta_cliente",
    #     ]
    #     df = pd.DataFrame(columns=columnas)
    #     carpeta_cliente = os.path.basename(folder_path)

    #     def process_single_file(file_name):
    #         file_path = os.path.join(folder_path, file_name)
    #         text = self.process_file_with_ocr(file_path)
    #         return self.handle_extracted_data(file_name, text, carpeta_cliente, month, year)

    #     file_names = [
    #         f
    #         for f in os.listdir(folder_path)
    #         if os.path.isfile(os.path.join(folder_path, f)) and any(f.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"])
    #     ]

    #     with ThreadPoolExecutor(max_workers=4) as executor:
    #         try:
    #             results = list(executor.map(process_single_file, file_names))
    #             df = pd.concat(results, ignore_index=True) if results else pd.DataFrame()
    #             self.processed_files += len(file_names)
    #             progress = int((self.processed_files / total_files) * 100)
    #             self.progressChanged.emit(progress)
    #         except Exception as e:
    #             self.failed_weeks.append(carpeta_cliente)
    #             self.error_logger.log_error(folder_path, f"Weekly Processing Error: {str(e)}")

    #     return df
        
    def process_weekly_files(self, folder_path, year, month, total_files):
        combined_df = pd.DataFrame()
        files = os.listdir(folder_path)

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            try:
                print(f"Procesando archivo: {file_name}")  # Log temporal
                ocr_text = self.process_file_with_ocr(file_path)
                print(f"Texto OCR: {ocr_text}")  # Log temporal
                extracted_data = self.handle_extracted_data(file_name, ocr_text, folder_path, month, year)
                print(f"Datos extraídos: {extracted_data}")  # Log temporal
                combined_df = pd.concat([combined_df, extracted_data], ignore_index=True)
            except Exception as e:
                self.error_logger.log_error(file_name, str(e))

        return combined_df
    def format_excel_headers(self, file_path, headers):
        try:
            wb = load_workbook(file_path)
            ws = wb["Resumen"]

            header_style = {
                "font": Font(name="Calibri", size=20, bold=False, color="000000"),
                "fill": PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"),
                "alignment": Alignment(horizontal="center", vertical="center"),
                "border": Border(
                    left=Side(style="thin"),
                    right=Side(style="thin"),
                    top=Side(style="thin"),
                    bottom=Side(style="thin"),
                ),
            }

            for col, header in enumerate(headers, start=1):
                cell = ws.cell(row=1, column=col, value=header)
                for attr, value in header_style.items():
                    setattr(cell, attr, value)

            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                ws.column_dimensions[column].width = max_length + 2

            wb.save(file_path)
            print(f"Encabezados formateados correctamente en el archivo: {file_path}")

        except Exception as e:
            print(f"Error al formatear los encabezados: {e}")

    def process(self, parent_folder, year, month):
        start_time = datetime.now()
        try:
            self.validate_inputs(parent_folder, year, month)
            payroll_folder_name = f"Payroll {year}"
            translated_month = self.translate_month(month)
            combined_df = pd.DataFrame()

            client_folders = [
                f
                for f in os.listdir(parent_folder)
                if os.path.isdir(os.path.join(parent_folder, f))
            ]
            total_files = sum(
                len(
                    [
                        f
                        for f in os.listdir(os.path.join(parent_folder, folder))
                        if any(f.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"])
                    ]
                )
                for folder in client_folders
            )

            for client_folder in client_folders:
                client_path = os.path.join(parent_folder, client_folder)
                target_path = self._get_target_path(client_path, payroll_folder_name, str(year), translated_month)
                if not target_path:
                    logging.warning(f"Carpeta no válida: {client_path}")
                    continue
                weekly_df = self.process_weekly_files(target_path, year, translated_month, total_files)
                if not weekly_df.empty:
                    combined_df = pd.concat([combined_df, weekly_df], ignore_index=True)
                else:
                    self.failed_weeks.append(client_folder)

            if not combined_df.empty:
                self.save_to_excel(os.path.join(self.output_folder, self.output_file), combined_df)

        except Exception as e:
            logging.critical(f"Error crítico: {e}")

        finally:
            end_time = datetime.now()
            self.generate_summary(start_time, end_time)
            self.error_logger.save_log()

    def save_to_excel(self, file_path, df_new):
        try:
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                df_new.to_excel(writer, index=False, sheet_name="Resumen")
            print(f"Datos guardados en el archivo Excel: {file_path}")
        except Exception as e:
            print(f"Error al guardar los datos en el archivo Excel: {e}")

    def generate_summary(self, start_time, end_time):
        summary = {
            "start_time": str(start_time),
            "end_time": str(end_time),
            "total_files_processed": self.processed_files,
            "failed_files": self.failed_files,
            "failed_weeks": self.failed_weeks,
        }
        summary_path = os.path.join(self.output_folder, "summary.json")
        with open(summary_path, "w") as summary_file:
            json.dump(summary, summary_file, indent=4)
        logging.info(f"Resumen guardado en {summary_path}")
