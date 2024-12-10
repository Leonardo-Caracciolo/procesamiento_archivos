# # import os
# # import pytesseract
# # import fitz  # PyMuPDF para trabajar con PDFs
# # from services.file_service import FileProcessor
# # from utils.validation_utils import validate_year_month
# # from PIL import Image
# # import services.func_extrac_data as look_data
# # import pandas as pd
# # import numpy as np

# # # Diccionario para traducir meses entre inglés y español
# # months_translator = {
# #     "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
# #     "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
# #     "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
# #     "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
# #     "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
# #     "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
# # }


# # class FolderProcessor:
# #     """
# #     Clase que procesa las carpetas de los clientes para buscar archivos específicos.
# #     """

# #     def __init__(self):
# #         self.file_processor = FileProcessor()

# #     def process(self, parent_folder, year, month):
# #         """
# #         Procesa las carpetas principales para buscar archivos relevantes.
# #         :param parent_folder: Ruta de la carpeta principal.
# #         :param year: Año seleccionado.
# #         :param month: Mes seleccionado.
# #         """
# #         validate_year_month(year, month)  # Validar el año y mes
# #         payroll_folder_name = f"Payroll {year}"
# #         year_folder_name = str(year)
# #         translated_month = self.translate_month(month)  # Traduce el mes al idioma necesario
# #         missing_folders = []

# #         ruta_archivo_fil = r'L:\Procesamiento_PDF\procesamiento_archivos\Data\Output\datos_filtrados.xlsx'
# #         ruta_archivo = r'L:\Procesamiento_PDF\procesamiento_archivos\Data\Output\datos.xlsx'

# #         for client_folder in os.listdir(parent_folder):
# #             client_path = os.path.join(parent_folder, client_folder)

# #             if not os.path.isdir(client_path):
# #                 continue

# #             target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name, translated_month)
# #             if not target_path:
# #                 missing_folders.append(client_path)
# #                 print(f"No se encontró carpeta válida en: {os.path.abspath(client_path)}")
# #                 continue

# #             print(f"Procesando carpeta: {os.path.abspath(target_path)}")
# #             df_weekly = self.process_weekly_files(target_path, year, translated_month)
# #             df_filtrado = self.group_by_weekly(df_weekly)

# #             # Guardar datos en los archivos Excel, anexando si ya existen
# #             self.save_to_excel(ruta_archivo, df_weekly)
# #             self.save_to_excel(ruta_archivo_fil, df_filtrado)

# #         if missing_folders:
# #             self._log_missing_folders(missing_folders, payroll_folder_name, year_folder_name, translated_month)

# #     def _get_target_path(self, client_path, payroll_folder_name, year_folder_name, month):
# #         """
# #         Busca la carpeta objetivo dentro del cliente.
# #         :param client_path: Ruta del cliente.
# #         :param payroll_folder_name: Nombre de la carpeta de nóminas.
# #         :param year_folder_name: Nombre de la carpeta del año.
# #         :param month: Mes traducido (en español o inglés).
# #         :return: Ruta de la carpeta objetivo o None.
# #         """
# #         possible_paths = [
# #             os.path.join(client_path, payroll_folder_name, f"11 - {month}"),
# #             os.path.join(client_path, year_folder_name, f"11 - {month}"),
# #             os.path.join(client_path, payroll_folder_name, month),
# #             os.path.join(client_path, year_folder_name, month),
# #             os.path.join(client_path, f"{year_folder_name} - {month}")
# #         ]

# #         for path in possible_paths:
# #             if os.path.exists(path):
# #                 return path
# #         return None

# #     def process_weekly_files(self, folder_path, year, month):
# #         """
# #         Procesa los archivos relevantes en una carpeta semanal.
# #         :param folder_path: Ruta de la carpeta.
# #         :param year: Año seleccionado.
# #         :param month: Mes traducido.
# #         """
# #         columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd', 
# #                     '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle']
# #         df = pd.DataFrame(columns=columnas)

# #         for file_name in os.listdir(folder_path):
# #             file_path = os.path.join(folder_path, file_name)

# #             if not os.path.isfile(file_path):
# #                 continue

# #             if not any(file_name.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"]):
# #                 continue

# #             print(f"Procesando archivo: {os.path.abspath(file_path)}")
# #             text = self.process_file_with_ocr(file_path)
# #             datos = self.handle_extracted_data(file_name, text, month, year)
# #             df = pd.concat([df, datos], ignore_index=True)

# #         return df

# #     def process_file_with_ocr(self, file_path):
# #         """
# #         Procesa un archivo PDF con OCR si no es editable.
# #         :param file_path: Ruta del archivo PDF.
# #         :return: Texto extraído.
# #         """
# #         try:
# #             pdf_document = fitz.open(file_path)
# #             extracted_text = ""
# #             last_page_number = len(pdf_document) - 1
# #             page = pdf_document[last_page_number]
# #             pix = page.get_pixmap(dpi=600)  # Renderizar página como imagen
# #             image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
# #             extracted_text += pytesseract.image_to_string(image, lang='spa', config='--dpi 600')
# #             return extracted_text
# #         except Exception as e:
# #             print(f"Error al procesar el archivo con OCR: {e}")
# #             return ""

# #     def handle_extracted_data(self, file_name, text, month, year):
# #         """
# #         Maneja los datos extraídos del texto según el tipo de archivo.
# #         """
# #         def format_date(date_str):
# #             try:
# #                 return pd.to_datetime(date_str).strftime('%Y-%m-%d')
# #             except ValueError:
# #                 return date_str

# #         if file_name.endswith("941.pdf"):
# #             data = {
# #                 'tipo_archivo': "941",
# #                 'fecha_pdf': file_name.replace('941.pdf', ''),
# #                 'Name': look_data.extract_payer_name(text),
# #                 '941_payment_amount': look_data.extract_payment_amount_941(text),
# #                 'account_number': look_data.extract_account_number(text),
# #                 'date_pay_settle': format_date(look_data.extract_settlement_date(text))
# #             }
# #         elif file_name.endswith("EDD.pdf"):
# #             data = {
# #                 'tipo_archivo': "EDD",
# #                 'fecha_pdf': file_name.replace('EDD.pdf', ''),
# #                 'Name': look_data.extract_name(text),
# #                 'EDD_payment_amount': look_data.extract_payment_amount_edd(text, 2),
# #                 'account_number': look_data.extract_account_number(text),
# #                 'date_pay_settle': format_date(look_data.extract_payment_date(text))
# #             }
# #         else:
# #             data = {
# #                 'tipo_archivo': "general",
# #                 'fecha_pdf': file_name.replace('.pdf', ''),
# #                 'Name': look_data.extract_company_name(text),
# #                 'federal_tax_941': look_data.extract_payment_amount_general_941(text),
# #                 'state_tax_edd': look_data.extract_payment_amount_general_edd(text)
# #             }

# #         return pd.DataFrame([data])

# #     def translate_month(self, month):
# #         """Traduce un mes entre inglés y español."""
# #         return months_translator.get(month, month)

# #     def _log_missing_folders(self, missing_folders, payroll_folder_name, year_folder_name, month):
# #         """
# #         Registra las carpetas faltantes en un archivo de log.
# #         """
# #         log_path = "missing_folders.log"
# #         with open(log_path, "w") as log_file:
# #             log_file.write("Carpetas faltantes:\n")
# #             for folder in missing_folders:
# #                 log_file.write(f"{os.path.abspath(folder)}\n")
# #             log_file.write("\nPatrones buscados:\n")
# #             log_file.write(f"{payroll_folder_name}/11 - {month}\n")
# #             log_file.write(f"{year_folder_name}/11 - {month}\n")
# #             log_file.write(f"{payroll_folder_name}/{month}\n")
# #             log_file.write(f"{year_folder_name}/{month}\n")
# #         print(f"Se ha generado un log de carpetas faltantes en: {log_path}")

# #     def group_by_weekly(self, dataframe):
# #         """
# #         Agrupa los datos semanalmente para consolidar información.
# #         """
# #         fechas_unicas = dataframe['fecha_pdf'].unique().tolist()
# #         resultados = []

# #         for fecha in fechas_unicas:
# #             df_filtrado = dataframe[dataframe['fecha_pdf'] == fecha]
# #             resultado = {'fecha_pdf': fecha}
# #             for columna in ['Name', 'federal_tax_941', 'state_tax_edd', '941_payment_amount', 'EDD_payment_amount']:
# #                 valores = df_filtrado[columna].replace('', np.nan).dropna()
# #                 resultado[columna] = valores.iloc[0] if not valores.empty else np.nan
# #             resultados.append(resultado)

# #         return pd.DataFrame(resultados)

# #     def save_to_excel(self, file_path, df_new):
# #         """
# #         Guarda un DataFrame en un archivo Excel, anexando si ya existe.
# #         """
# #         if os.path.exists(file_path):
# #             try:
# #                 df_existing = pd.read_excel(file_path)
# #             except Exception as e:
# #                 print(f"Error al leer el archivo existente: {e}")
# #                 df_existing = pd.DataFrame()

# #             df_combined = pd.concat([df_existing, df_new], ignore_index=True)
# #         else:
# #             df_combined = df_new

# #         try:
# #             df_combined.to_excel(file_path, index=False)
# #             print(f"Datos guardados en {file_path}")
# #         except Exception as e:
# #             print(f"Error al guardar los datos en el archivo Excel: {e}")



# #--------------------Funcional
# # import os
# # import pytesseract
# # import fitz  # PyMuPDF para trabajar con PDFs
# # from services.file_service import FileProcessor
# # from utils.validation_utils import validate_year_month
# # from PIL import Image
# # import services.func_extrac_data as look_data
# # import pandas as pd
# # import numpy as np

# # # Diccionario para traducir meses entre inglés y español
# # months_translator = {
# #     "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
# #     "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
# #     "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
# #     "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
# #     "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
# #     "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
# # }

# # class FolderProcessor:
# #     """
# #     Clase que procesa las carpetas de los clientes para buscar archivos específicos.
# #     """

# #     def __init__(self):
# #         self.file_processor = FileProcessor()

# #     def process(self, parent_folder, year, month):
# #         """
# #         Procesa las carpetas principales para buscar archivos relevantes.
# #         :param parent_folder: Ruta de la carpeta principal.
# #         :param year: Año seleccionado.
# #         :param month: Mes seleccionado.
# #         """
# #         validate_year_month(year, month)  # Validar el año y mes
# #         payroll_folder_name = f"Payroll {year}"
# #         year_folder_name = str(year)
# #         translated_month = self.translate_month(month)  # Traduce el mes al idioma necesario
# #         missing_folders = []

# #         ruta_archivo_fil = r'L:\Procesamiento_PDF\procesamiento_archivos\Data\Output\datos_filtrados.xlsx'
# #         ruta_archivo = r'L:\Procesamiento_PDF\procesamiento_archivos\Data\Output\datos.xlsx'

# #         for client_folder in os.listdir(parent_folder):
# #             client_path = os.path.join(parent_folder, client_folder)

# #             if not os.path.isdir(client_path):
# #                 continue

# #             target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name, translated_month)
# #             if not target_path:
# #                 missing_folders.append(client_path)
# #                 print(f"No se encontró carpeta válida en: {os.path.abspath(client_path)}")
# #                 continue

# #             print(f"Procesando carpeta: {os.path.abspath(target_path)}")
# #             df_weekly = self.process_weekly_files(target_path, year, translated_month)
# #             df_filtrado = self.group_by_weekly(df_weekly)

# #             # Mostrar los DataFrames generados por pantalla
# #             print(f"\nDataFrame semanal para {target_path}:")
# #             print(df_weekly)

# #             print(f"\nDataFrame filtrado para {target_path}:")
# #             print(df_filtrado)

# #             # Guardar datos en los archivos Excel, anexando si ya existen
# #             self.save_to_excel(ruta_archivo, df_weekly)
# #             self.save_to_excel(ruta_archivo_fil, df_filtrado)

# #         if missing_folders:
# #             self._log_missing_folders(missing_folders, payroll_folder_name, year_folder_name, translated_month)

# #     def _get_target_path(self, client_path, payroll_folder_name, year_folder_name, month):
# #         """
# #         Busca la carpeta objetivo dentro del cliente.
# #         :param client_path: Ruta del cliente.
# #         :param payroll_folder_name: Nombre de la carpeta de nóminas.
# #         :param year_folder_name: Nombre de la carpeta del año.
# #         :param month: Mes traducido (en español o inglés).
# #         :return: Ruta de la carpeta objetivo o None.
# #         """
# #         possible_paths = [
# #             os.path.join(client_path, payroll_folder_name, f"11 - {month}"),
# #             os.path.join(client_path, year_folder_name, f"11 - {month}"),
# #             os.path.join(client_path, payroll_folder_name, month),
# #             os.path.join(client_path, year_folder_name, month),
# #             os.path.join(client_path, f"{year_folder_name} - {month}")
# #         ]

# #         for path in possible_paths:
# #             if os.path.exists(path):
# #                 return path
# #         return None

# #     def process_weekly_files(self, folder_path, year, month):
# #         """
# #         Procesa los archivos relevantes en una carpeta semanal.
# #         :param folder_path: Ruta de la carpeta.
# #         :param year: Año seleccionado.
# #         :param month: Mes traducido.
# #         """
# #         columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd', 
# #                     '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle']
# #         df = pd.DataFrame(columns=columnas)

# #         for file_name in os.listdir(folder_path):
# #             file_path = os.path.join(folder_path, file_name)

# #             if not os.path.isfile(file_path):
# #                 continue

# #             if not any(file_name.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"]):
# #                 continue

# #             print(f"Procesando archivo: {os.path.abspath(file_path)}")
# #             text = self.process_file_with_ocr(file_path)
# #             datos = self.handle_extracted_data(file_name, text, month, year)
# #             print(f"\nDataFrame para {file_name}:")
# #             print(datos)
# #             df = pd.concat([df, datos], ignore_index=True)

# #         return df

# #     def process_file_with_ocr(self, file_path):
# #         """
# #         Procesa un archivo PDF con OCR si no es editable.
# #         :param file_path: Ruta del archivo PDF.
# #         :return: Texto extraído.
# #         """
# #         try:
# #             pdf_document = fitz.open(file_path)
# #             extracted_text = ""
# #             last_page_number = len(pdf_document) - 1
# #             page = pdf_document[last_page_number]
# #             pix = page.get_pixmap(dpi=600)  # Renderizar página como imagen
# #             image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
# #             extracted_text += pytesseract.image_to_string(image, lang='spa', config='--dpi 600')
# #             return extracted_text
# #         except Exception as e:
# #             print(f"Error al procesar el archivo con OCR: {e}")
# #             return ""

# #     def handle_extracted_data(self, file_name, text, month, year):
# #         """
# #         Maneja los datos extraídos del texto según el tipo de archivo.
# #         """
# #         def format_date(date_str):
# #             try:
# #                 return pd.to_datetime(date_str).strftime('%Y-%m-%d')
# #             except ValueError:
# #                 return date_str

# #         if file_name.endswith("941.pdf"):
# #             data = {
# #                 'tipo_archivo': "941",
# #                 'fecha_pdf': file_name.replace('941.pdf', ''),
# #                 'Name': look_data.extract_payer_name(text),
# #                 '941_payment_amount': look_data.extract_payment_amount_941(text),
# #                 'account_number': look_data.extract_account_number(text),
# #                 'date_pay_settle': format_date(look_data.extract_settlement_date(text))
# #             }
# #         elif file_name.endswith("EDD.pdf"):
# #             data = {
# #                 'tipo_archivo': "EDD",
# #                 'fecha_pdf': file_name.replace('EDD.pdf', ''),
# #                 'Name': look_data.extract_name(text),
# #                 'EDD_payment_amount': look_data.extract_payment_amount_edd(text, 2),
# #                 'account_number': look_data.extract_account_number(text),
# #                 'date_pay_settle': format_date(look_data.extract_payment_date(text))
# #             }
# #         else:
# #             data = {
# #                 'tipo_archivo': "general",
# #                 'fecha_pdf': file_name.replace('.pdf', ''),
# #                 'Name': look_data.extract_company_name(text),
# #                 'federal_tax_941': look_data.extract_payment_amount_general_941(text),
# #                 'state_tax_edd': look_data.extract_payment_amount_general_edd(text)
# #             }

# #         return pd.DataFrame([data])

# #     def translate_month(self, month):
# #         """Traduce un mes entre inglés y español."""
# #         return months_translator.get(month, month)

# #     def _log_missing_folders(self, missing_folders, payroll_folder_name, year_folder_name, month):
# #         """
# #         Registra las carpetas faltantes en un archivo de log.
# #         """
# #         log_path = "missing_folders.log"
# #         with open(log_path, "w") as log_file:
# #             log_file.write("Carpetas faltantes:\n")
# #             for folder in missing_folders:
# #                 log_file.write(f"{os.path.abspath(folder)}\n")
# #             log_file.write("\nPatrones buscados:\n")
# #             log_file.write(f"{payroll_folder_name}/11 - {month}\n")
# #             log_file.write(f"{year_folder_name}/11 - {month}\n")
# #             log_file.write(f"{payroll_folder_name}/{month}\n")
# #             log_file.write(f"{year_folder_name}/{month}\n")
# #         print(f"Se ha generado un log de carpetas faltantes en: {log_path}")

# #     def group_by_weekly(self, dataframe):
# #         """
# #         Agrupa los datos semanalmente para consolidar información.
# #         """
# #         fechas_unicas = dataframe['fecha_pdf'].unique().tolist()
# #         resultados = []

# #         for fecha in fechas_unicas:
# #             df_filtrado = dataframe[dataframe['fecha_pdf'] == fecha]
# #             resultado = {'fecha_pdf': fecha}
# #             for columna in ['Name', 'federal_tax_941', 'state_tax_edd', '941_payment_amount', 'EDD_payment_amount']:
# #                 valores = df_filtrado[columna].replace('', np.nan).dropna()
# #                 resultado[columna] = valores.iloc[0] if not valores.empty else np.nan
# #             resultados.append(resultado)

# #         return pd.DataFrame(resultados)

# #     def save_to_excel(self, file_path, df_new):
# #         """
# #         Guarda un DataFrame en un archivo Excel, anexando si ya existe.
# #         """
# #         if os.path.exists(file_path):
# #             try:
# #                 df_existing = pd.read_excel(file_path)
# #             except Exception as e:
# #                 print(f"Error al leer el archivo existente: {e}")
# #                 df_existing = pd.DataFrame()

# #             df_combined = pd.concat([df_existing, df_new], ignore_index=True)
# #         else:
# #             df_combined = df_new

# #         try:
# #             df_combined.to_excel(file_path, index=False)
# #             print(f"Datos guardados en {file_path}")
# #         except Exception as e:
# #             print(f"Error al guardar los datos en el archivo Excel: {e}")






# import os
# import pytesseract
# import fitz  # PyMuPDF para trabajar con PDFs
# from PIL import Image
# import pandas as pd
# import numpy as np
# from datetime import datetime

# # Diccionario para traducir meses entre inglés y español
# months_translator = {
#     "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
#     "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
#     "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
#     "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
#     "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
#     "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
# }


# class FolderProcessor:
#     """
#     Clase que procesa las carpetas de los clientes para buscar archivos específicos.
#     """

#     def __init__(self, output_folder):
#         self.output_folder = output_folder  # Carpeta donde se guardarán los .xlsx
#         os.makedirs(output_folder, exist_ok=True)  # Crear carpeta de salida si no existe

#     def process(self, parent_folder, year, month):
#         """
#         Procesa las carpetas principales para buscar archivos relevantes.
#         """
#         payroll_folder_name = f"Payroll {year}"
#         year_folder_name = str(year)
#         translated_month = self.translate_month(month)  # Traduce el mes al idioma necesario
#         missing_folders = []

#         for client_folder in os.listdir(parent_folder):
#             client_path = os.path.join(parent_folder, client_folder)

#             if not os.path.isdir(client_path):
#                 continue

#             target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name, translated_month)
#             if not target_path:
#                 missing_folders.append(client_path)
#                 print(f"No se encontró carpeta válida en: {os.path.abspath(client_path)}")
#                 continue

#             print(f"Procesando carpeta: {os.path.abspath(target_path)}")
#             df_weekly = self.process_weekly_files(target_path, year, translated_month)

#             # Guardar los datos
#             output_xlsx_path = os.path.join(self.output_folder, f"{client_folder}_datos.xlsx")
#             self.save_to_excel(output_xlsx_path, df_weekly)

#         if missing_folders:
#             self._log_missing_folders(missing_folders, payroll_folder_name, year_folder_name, translated_month)

#     def _get_target_path(self, client_path, payroll_folder_name, year_folder_name, month):
#         """
#         Busca la carpeta objetivo dentro del cliente.
#         """
#         possible_paths = [
#             os.path.join(client_path, payroll_folder_name, f"11 - {month}"),
#             os.path.join(client_path, year_folder_name, f"11 - {month}"),
#             os.path.join(client_path, payroll_folder_name, month),
#             os.path.join(client_path, year_folder_name, month),
#             os.path.join(client_path, f"{year_folder_name} - {month}")
#         ]

#         for path in possible_paths:
#             if os.path.exists(path):
#                 return path
#         return None

#     def process_weekly_files(self, folder_path, year, month):
#         """
#         Procesa los archivos relevantes en una carpeta semanal.
#         """
#         columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd', 
#                     '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle']
#         df = pd.DataFrame(columns=columnas)

#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)

#             if not os.path.isfile(file_path):
#                 continue

#             if not any(file_name.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"]):
#                 continue

#             print(f"Procesando archivo: {os.path.abspath(file_path)}")
#             text = self.process_file_with_ocr(file_path)

#             # Guardar texto extraído en archivo .txt en la carpeta procesada
#             txt_path = os.path.join(folder_path, file_name.replace(".pdf", ".txt"))
#             with open(txt_path, "w", encoding="utf-8") as txt_file:
#                 txt_file.write(text)

#             datos = self.handle_extracted_data(file_name, text, month, year)

#             # Guardar log individual para cada archivo
#             log_path = os.path.join(folder_path, file_name.replace(".pdf", "_log.txt"))
#             self.save_log_for_file(log_path, datos, file_name)

#             df = pd.concat([df, datos], ignore_index=True)

#         return df

#     def process_file_with_ocr(self, file_path):
#         """
#         Procesa un archivo PDF con OCR si no es editable.
#         """
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

#     def handle_extracted_data(self, file_name, text, month, year):
#         """
#         Maneja los datos extraídos del texto según el tipo de archivo.
#         """
#         if file_name.endswith("941.pdf"):
#             return pd.DataFrame([{
#                 'tipo_archivo': "941",
#                 'fecha_pdf': file_name.replace('941.pdf', ''),
#                 'Name': "Ejemplo Name",  # Aquí incluir la lógica específica
#                 '941_payment_amount': "12345.67",  # Aquí incluir la lógica específica
#                 'account_number': "123456",  # Aquí incluir la lógica específica
#                 'date_pay_settle': "2024-12-31"  # Aquí incluir la lógica específica
#             }])
#         elif file_name.endswith("EDD.pdf"):
#             return pd.DataFrame([{
#                 'tipo_archivo': "EDD",
#                 'fecha_pdf': file_name.replace('EDD.pdf', ''),
#                 'Name': "Ejemplo Name",  # Aquí incluir la lógica específica
#                 'EDD_payment_amount': "123.45",  # Aquí incluir la lógica específica
#                 'account_number': "123456",  # Aquí incluir la lógica específica
#                 'date_pay_settle': "2024-12-31"  # Aquí incluir la lógica específica
#             }])
#         else:
#             return pd.DataFrame([{
#                 'tipo_archivo': "general",
#                 'fecha_pdf': file_name.replace('.pdf', ''),
#                 'Name': "Ejemplo Name",  # Aquí incluir la lógica específica
#                 'federal_tax_941': "123.45",  # Aquí incluir la lógica específica
#                 'state_tax_edd': "678.90"  # Aquí incluir la lógica específica
#             }])

#     def save_log_for_file(self, log_path, datos, file_name):
#         """
#         Guarda un log individual para cada archivo procesado.
#         """
#         with open(log_path, "w", encoding="utf-8") as log_file:
#             log_file.write(f"Log de campos obtenidos para el archivo: {file_name}\n")
#             log_file.write("=" * 50 + "\n")
#             log_file.write(datos.to_string(index=False))
#         print(f"Log generado: {log_path}")

#     def save_to_excel(self, file_path, df_new):
#         """
#         Guarda un DataFrame en un archivo Excel, anexando si ya existe.
#         """
#         if os.path.exists(file_path):
#             try:
#                 df_existing = pd.read_excel(file_path)
#             except Exception as e:
#                 print(f"Error al leer el archivo existente: {e}")
#                 df_existing = pd.DataFrame()

#             df_combined = pd.concat([df_existing, df_new], ignore_index=True)
#         else:
#             df_combined = df_new

#         try:
#             df_combined.to_excel(file_path, index=False)
#             print(f"Datos guardados en {file_path}")
#         except Exception as e:
#             print(f"Error al guardar los datos en el archivo Excel: {e}")

#     def _log_missing_folders(self, missing_folders, payroll_folder_name, year_folder_name, month):
#         """
#         Registra las carpetas faltantes en un archivo de log.
#         """
#         log_path = os.path.join(self.output_folder, "missing_folders.log")
#         with open(log_path, "w") as log_file:
#             log_file.write("Carpetas faltantes:\n")
#             for folder in missing_folders:
#                 log_file.write(f"{os.path.abspath(folder)}\n")
#         print(f"Se ha generado un log de carpetas faltantes en: {log_path}")

#     def translate_month(self, month):
#         """Traduce un mes entre inglés y español."""
#         return months_translator.get(month, month)



import os
import pytesseract
import fitz  # PyMuPDF para trabajar con PDFs
from PIL import Image
import pandas as pd
import numpy as np
import services.func_extrac_data as look_data  # Asegúrate de que esta ruta sea correcta

# Diccionario para traducir meses entre inglés y español
months_translator = {
    "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
    "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
    "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
    "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
    "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
    "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
}


class FolderProcessor:
    """
    Clase que procesa las carpetas de los clientes para buscar archivos específicos.
    """

    def __init__(self, output_folder):
        self.output_folder = output_folder  # Carpeta donde se guardarán los .xlsx
        os.makedirs(output_folder, exist_ok=True)  # Crear carpeta de salida si no existe

    def process(self, parent_folder, year, month):
        """
        Procesa las carpetas principales para buscar archivos relevantes.
        """
        payroll_folder_name = f"Payroll {year}"
        year_folder_name = str(year)
        translated_month = self.translate_month(month)  # Traduce el mes al idioma necesario
        missing_folders = []

        for client_folder in os.listdir(parent_folder):
            client_path = os.path.join(parent_folder, client_folder)

            if not os.path.isdir(client_path):
                continue

            target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name, translated_month)
            if not target_path:
                missing_folders.append(client_path)
                print(f"No se encontró carpeta válida en: {os.path.abspath(client_path)}")
                continue

            print(f"Procesando carpeta: {os.path.abspath(target_path)}")
            df_weekly = self.process_weekly_files(target_path, year, translated_month)

            # Guardar los datos
            output_xlsx_path = os.path.join(self.output_folder, f"{client_folder}_datos.xlsx")
            self.save_to_excel(output_xlsx_path, df_weekly)

        if missing_folders:
            self._log_missing_folders(missing_folders, payroll_folder_name, year_folder_name, translated_month)

    def _get_target_path(self, client_path, payroll_folder_name, year_folder_name, month):
        """
        Busca la carpeta objetivo dentro del cliente.
        """
        possible_paths = [
            os.path.join(client_path, payroll_folder_name, f"11 - {month}"),
            os.path.join(client_path, year_folder_name, f"11 - {month}"),
            os.path.join(client_path, payroll_folder_name, month),
            os.path.join(client_path, year_folder_name, month),
            os.path.join(client_path, f"{year_folder_name} - {month}")
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def process_weekly_files(self, folder_path, year, month):
        """
        Procesa los archivos relevantes en una carpeta semanal.
        """
        columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd',
                    '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle']
        df = pd.DataFrame(columns=columnas)

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(file_path):
                continue

            if not any(file_name.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"]):
                continue

            print(f"Procesando archivo: {os.path.abspath(file_path)}")
            text = self.process_file_with_ocr(file_path)

            # Guardar texto extraído en archivo .txt en la carpeta procesada
            txt_path = os.path.join(folder_path, file_name.replace(".pdf", ".txt"))
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)

            datos = self.handle_extracted_data(file_name, text, month, year)

            # Guardar log individual para cada archivo
            log_path = os.path.join(folder_path, file_name.replace(".pdf", "_log.txt"))
            self.save_log_for_file(log_path, datos, file_name)

            df = pd.concat([df, datos], ignore_index=True)

        return df

    def process_file_with_ocr(self, file_path):
        """
        Procesa un archivo PDF con OCR si no es editable.
        """
        try:
            pdf_document = fitz.open(file_path)
            extracted_text = ""
            last_page_number = len(pdf_document) - 1
            page = pdf_document[last_page_number]
            pix = page.get_pixmap(dpi=600)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            extracted_text += pytesseract.image_to_string(image, lang='spa', config='--dpi 600')
            return extracted_text
        except Exception as e:
            print(f"Error al procesar el archivo con OCR: {e}")
            return ""

    def handle_extracted_data(self, file_name, text, month, year):
        """
        Maneja los datos extraídos del texto según el tipo de archivo.
        """
        def format_date(date_str):
            try:
                return pd.to_datetime(date_str).strftime('%Y-%m-%d')
            except ValueError:
                return date_str

        if file_name.endswith("941.pdf"):
            print(f"Extrayendo datos del archivo: {file_name}")
            return pd.DataFrame([{
                'tipo_archivo': "941",
                'fecha_pdf': file_name.replace('941.pdf', ''),
                'Name': look_data.extract_payer_name(text),
                '941_payment_amount': look_data.extract_payment_amount_941(text),
                'account_number': look_data.extract_account_number(text),
                'date_pay_settle': format_date(look_data.extract_settlement_date(text))
            }])
        elif file_name.endswith("EDD.pdf"):
            print(f"Extrayendo datos del archivo: {file_name}")
            return pd.DataFrame([{
                'tipo_archivo': "EDD",
                'fecha_pdf': file_name.replace('EDD.pdf', ''),
                'Name': look_data.extract_name(text),
                'EDD_payment_amount': look_data.extract_payment_amount_edd(text, 2),
                'account_number': look_data.extract_account_number(text),
                'date_pay_settle': format_date(look_data.extract_payment_date(text))
            }])
        else:
            print(f"Extrayendo datos del archivo: {file_name}")
            return pd.DataFrame([{
                'tipo_archivo': "general",
                'fecha_pdf': file_name.replace('.pdf', ''),
                'Name': look_data.extract_company_name(text),
                'federal_tax_941': look_data.extract_payment_amount_general_941(text),
                'state_tax_edd': look_data.extract_payment_amount_general_edd(text)
            }])

    def save_log_for_file(self, log_path, datos, file_name):
        """
        Guarda un log individual para cada archivo procesado.
        """
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(f"Log de campos obtenidos para el archivo: {file_name}\n")
            log_file.write("=" * 50 + "\n")
            log_file.write(datos.to_string(index=False))
        print(f"Log generado: {log_path}")

    def save_to_excel(self, file_path, df_new):
        """
        Guarda un DataFrame en un archivo Excel, anexando si ya existe.
        """
        if os.path.exists(file_path):
            try:
                df_existing = pd.read_excel(file_path)
            except Exception as e:
                print(f"Error al leer el archivo existente: {e}")
                df_existing = pd.DataFrame()

            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new

        try:
            df_combined.to_excel(file_path, index=False)
            print(f"Datos guardados en {file_path}")
        except Exception as e:
            print(f"Error al guardar los datos en el archivo Excel: {e}")

    def _log_missing_folders(self, missing_folders, payroll_folder_name, year_folder_name, month):
        """
        Registra las carpetas faltantes en un archivo de log.
        """
        log_path = os.path.join(self.output_folder, "missing_folders.log")
        with open(log_path, "w") as log_file:
            log_file.write("Carpetas faltantes:\n")
            for folder in missing_folders:
                log_file.write(f"{os.path.abspath(folder)}\n")
        print(f"Se ha generado un log de carpetas faltantes en: {log_path}")

    def translate_month(self, month):
        """Traduce un mes entre inglés y español."""
        return months_translator.get(month, month)

