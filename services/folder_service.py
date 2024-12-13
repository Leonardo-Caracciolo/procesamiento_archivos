# import os
# import pytesseract
# import fitz  # PyMuPDF para trabajar con PDFs
# from PIL import Image
# import pandas as pd
# import numpy as np
# import services.func_extrac_data as look_data  # Asegúrate de que esta ruta sea correcta
# from openpyxl import load_workbook
# from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# from PyQt5.QtCore import QObject, pyqtSignal



# # Diccionario para traducir meses entre inglés y español
# months_translator = {
#     "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
#     "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
#     "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
#     "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
#     "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
#     "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
# }

# class FolderProcessor(QObject):
#     progressChanged = pyqtSignal(int)
#     def __init__(self, output_folder, output_file):
#         self.output_folder = output_folder  # Carpeta donde se guardarán los archivos
#         self.output_file = output_file  # Archivo Excel final
#         os.makedirs(output_folder, exist_ok=True)  # Crear carpeta de salida si no existe

#     def process(self, parent_folder, year, month):
#         payroll_folder_name = f"Payroll {year}"
#         year_folder_name = str(year)
#         translated_month = self.translate_month(month)  # Traduce el mes al idioma necesario
#         combined_df = pd.DataFrame()

#         for client_folder in os.listdir(parent_folder):
#             client_path = os.path.join(parent_folder, client_folder)

#             if not os.path.isdir(client_path):
#                 continue

#             target_path = self._get_target_path(client_path, payroll_folder_name, year_folder_name, translated_month)
#             if not target_path:
#                 print(f"No se encontró carpeta válida en: {os.path.abspath(client_path)}")
#                 continue

#             print(f"Procesando carpeta: {os.path.abspath(target_path)}")
#             df_weekly = self.process_weekly_files(target_path, year, translated_month)
#             combined_df = pd.concat([combined_df, df_weekly], ignore_index=True)

#         df_modify = self.prepare_data(combined_df)
#         # Guardar todos los datos combinados en un solo archivo Excel
#         self.save_to_excel(os.path.join(self.output_folder, self.output_file), df_modify)

#     def _get_target_path(self, client_path, payroll_folder_name, year_folder_name, month):
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
#         columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd',
#                     '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle','carpeta_cliente']
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

#         return df

import os
import pytesseract
import fitz  # PyMuPDF para trabajar con PDFs
from PIL import Image
import pandas as pd
import numpy as np
import services.func_extrac_data as look_data  # Asegúrate de que esta ruta sea correcta
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

from PyQt5.QtCore import QObject, pyqtSignal, QThread

# Diccionario para traducir meses entre inglés y español
months_translator = {
    "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
    "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
    "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
    "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
    "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
    "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
}

months_numbers = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
    "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
    "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}


class FolderProcessor(QObject):
    progressChanged = pyqtSignal(int)
    
    def __init__(self, output_folder, output_file):
        super().__init__()  # Llamar al constructor de QObject
        self.output_folder = output_folder  # Carpeta donde se guardarán los archivos
        self.output_file = output_file  # Archivo Excel final
        os.makedirs(output_folder, exist_ok=True)  # Crear carpeta de salida si no existe

    def process(self, parent_folder, year, month):
        payroll_folder_name = f"Payroll {year}"
        year_folder_name = str(year)
        translated_month = self.translate_month(month)  # Traduce el mes al idioma necesario
        month_number = self.get_month_number(month)
        combined_df = pd.DataFrame()

        client_folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
        total_folders = len(client_folders)
        total_files = 0
        self.processed_files = 0

        # Contar todos los archivos que se van a procesar
        for client_folder in client_folders:
            client_path = os.path.join(parent_folder, client_folder)
            target_path = self._get_target_path(client_path, year_folder_name, translated_month, month_number)
            if not target_path:
                continue
            total_files += len([f for f in os.listdir(target_path) if any(f.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"])])

        for client_folder in client_folders:
            client_path = os.path.join(parent_folder, client_folder)
            target_path = self._get_target_path(client_path, year_folder_name, translated_month, month_number)
            if not target_path:
                print(f"No se encontró carpeta válida en: {os.path.abspath(client_path)}")
                continue

            print(f"Procesando carpeta: {os.path.abspath(target_path)}")
            df_weekly = self.process_weekly_files(target_path, year, translated_month, total_files, self.processed_files)
            combined_df = pd.concat([combined_df, df_weekly], ignore_index=True)

        df_modify = self.prepare_data(combined_df)
        # Guardar todos los datos combinados en un solo archivo Excel
        self.save_to_excel(os.path.join(self.output_folder, self.output_file), df_modify)

    def clean_path_segment(self, segment):
        # Reemplazar espacios en "mes-numero" para que quede "numero_mes+mes"
        return segment.replace(" ", "")
    
    def _get_target_path(self, path, year, month, number):

        year_folder = None
        
        for root, dirs, files in os.walk(path):
            for name in dirs:
                if str(year) in name and "Payroll" in name:
                    year_folder = os.path.join(root, name)
                elif str(year) in name and "payroll" in name:
                    year_folder = os.path.join(root, name)
                elif str(year) in name:
                        year_folder = os.path.join(root, name)

        if year_folder is not None: 
            for root, dirs, files in os.walk(year_folder):
                for name in dirs:
                    if str(number) in name and month in name:
                        return os.path.join(root, name)
                    elif str(number) in name:
                        return os.path.join(root, name)
        return None



    def process_weekly_files(self, folder_path, year, month, total_files, processed_files):
        columnas = ['tipo_archivo', 'fecha_pdf', 'Name', 'federal_tax_941', 'state_tax_edd',
                    '941_payment_amount', 'EDD_payment_amount', 'account_number', 'date_pay_settle', 'carpeta_cliente']
        df = pd.DataFrame(columns=columnas)
        carpeta_cliente = os.path.basename(os.path.dirname(os.path.dirname(folder_path)))
        print(carpeta_cliente)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(file_path):
                continue

            if not any(file_name.endswith(suffix + ".pdf") for suffix in ["EDD", "941", f"{year}"]):
                continue

            print(f"Procesando archivo: {os.path.abspath(file_path)}")
            text = self.process_file_with_ocr(file_path)
            datos = self.handle_extracted_data(file_name, text, carpeta_cliente, month, year)

            df = pd.concat([df, datos], ignore_index=True)

            # Actualizar el progreso y emitir la señal
            self.processed_files += 1
            progress = int((self.processed_files / total_files) * 100)
            self.progressChanged.emit(progress)

        return df


    def process_file_with_ocr(self, file_path):
        try:
            pdf_document = fitz.open(file_path)
            extracted_text = ""
            last_page_number = len(pdf_document) - 1
            page = pdf_document[last_page_number]
            pix = page.get_pixmap(dpi=1200)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            extracted_text += pytesseract.image_to_string(image, lang='spa', config='--dpi 1200')
            return extracted_text
        except Exception as e:
            print(f"Error al procesar el archivo con OCR: {e}")
            return ""

    def handle_extracted_data(self, file_name, text, carpeta_cliente, month, year):
        def format_date(date_str):
            if date_str is None:
                return "0"
            
            try:
                return pd.to_datetime(date_str).strftime('%Y-%m-%d')
            except ValueError:
                return date_str

        if file_name.endswith("941.pdf"):
            return pd.DataFrame([{
                'tipo_archivo': "941",
                'fecha_pdf': file_name.replace('941.pdf', ''),
                'Name': look_data.extract_payer_name(text),
                '941_payment_amount': look_data.extract_payment_amount_941(text),
                'account_number': look_data.extract_account_number(text),
                'date_pay_settle': format_date(look_data.extract_settlement_date(text)),
                'carpeta_cliente': carpeta_cliente
            }])
        elif file_name.endswith("EDD.pdf"):
            return pd.DataFrame([{
                'tipo_archivo': "EDD",
                'fecha_pdf': file_name.replace('EDD.pdf', ''),
                'Name': look_data.extract_name(text),
                'EDD_payment_amount': look_data.extract_payment_amount_edd(text, 2),
                'account_number': look_data.extract_account_number(text),
                'date_pay_settle': format_date(look_data.extract_payment_date(text)),
                'carpeta_cliente': carpeta_cliente
            }])
        else:
            return pd.DataFrame([{
                'tipo_archivo': "general",
                'fecha_pdf': file_name.replace('.pdf', ''),
                'Name': look_data.extract_company_name(text),
                'federal_tax_941': look_data.extract_payment_amount_general_941(text),
                'state_tax_edd': look_data.extract_payment_amount_general_edd(text),
                'carpeta_cliente': carpeta_cliente
            }])

    def group_by_weekly(self, dataframe):
        """
        Agrupa los datos por carpeta_cliente y fecha_pdf para consolidar información.
        """

        dataframe['Check date'] = dataframe['Check date'].astype(int)
        # Obtener combinaciones únicas de 'carpeta_cliente' y 'fecha_pdf'
        combinaciones_unicas = dataframe[['Company', 'Check date']].drop_duplicates()

        resultados = []
        
        for _, fila in combinaciones_unicas.iterrows():
            carpeta_cliente = fila['Company']
            fecha = fila['Check date']
            df_filtrado = dataframe[(dataframe['Company'] == carpeta_cliente) & (dataframe['Check date'] == fecha)]
            resultado = {'Company': carpeta_cliente, 'Check date': fecha}
            
            for columna in ['Federal Tax', 'State Tax', 'Payment date' ,'941', 'EDD']:
                valores = df_filtrado[columna].replace('', np.nan).dropna()
                resultado[columna] = valores.iloc[0] if not valores.empty else np.nan
            
            resultados.append(resultado)

        return pd.DataFrame(resultados)

    def format_excel_headers(self, file_path, headers):
        """
        Formatea los encabezados de un archivo Excel con las especificaciones proporcionadas.
        
        :param file_path: Ruta al archivo Excel.
        :param headers: Lista de encabezados que se esperan en la primera fila.
        """
        try:
            # Cargar el archivo Excel
            wb = load_workbook(file_path)
            ws = wb["Resumen"]

            # Configuración de estilo
            header_style = {
                "font": Font(name="Calibri", size=20, bold=False, color="000000"),
                "fill": PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"),
                "alignment": Alignment(horizontal="center", vertical="center"),
                "border": Border(
                    left=Side(style="thin"),
                    right=Side(style="thin"),
                    top=Side(style="thin"),
                    bottom=Side(style="thin")
                )
            }

            # Aplicar formato a los encabezados
            for col, header in enumerate(headers, start=1):
                cell = ws.cell(row=1, column=col, value=header)
                for attr, value in header_style.items():
                    setattr(cell, attr, value)

            # Ajustar automáticamente el ancho de las columnas
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter  # Obtiene la letra de la columna
                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column].width = adjusted_width

            # Guardar los cambios en el archivo
            wb.save(file_path)
            print(f"Encabezados formateados correctamente en el archivo: {file_path}")

        except Exception as e:
            print(f"Error al formatear los encabezados: {e}")


    def crossamounts(self, path_file):
        """
        Inserta fórmulas en las columnas Balance 941 y Balance EDD.
        """
        # Seleccionar archivo Excel
        excel_path = path_file

        # Abrir el archivo Excel con openpyxl
        try:
            wb = load_workbook(excel_path)
            ws = wb['Resumen']

            ws.cell(1,8).value = 'Balance 941'
            ws.cell(1,9).value = 'Balance EDD'

            # Insertar fórmulas en las columnas H y I
            for row in range(2, ws.max_row + 1):  # Asume que la fila 1 es el encabezado
                ws[f"H{row}"] = f"=C{row}-F{row}"  # Balance 941
                ws[f"I{row}"] = f"=D{row}-G{row}"  # Balance EDD

            # Guardar cambios
            wb.save(excel_path)
            print("Fórmulas ingresadas en el archivo Excel.")
        except Exception as e:
            print("Error al cargar la formula")


    def prepare_data(self, df):

        df = pd.DataFrame(df)

        df['federal_tax_941'] = df['federal_tax_941'].str.replace(',', '')
        df['federal_tax_941'] = df['federal_tax_941'].str.replace('.', ',')

        df['state_tax_edd'] = df['state_tax_edd'].str.replace(',', '')
        df['state_tax_edd'] = df['state_tax_edd'].str.replace('.', ',')

        df['941_payment_amount'] = df['941_payment_amount'].str.replace(',', '')
        df['941_payment_amount'] = df['941_payment_amount'].str.replace('.', ',')

        df['EDD_payment_amount'] = df['EDD_payment_amount'].str.replace(',', '')
        df['EDD_payment_amount'] = df['EDD_payment_amount'].str.replace('.', ',')


        df = df.rename(columns={
            'carpeta_cliente': 'Company',
            'fecha_pdf': 'Check date',
            'federal_tax_941': 'Federal Tax',
            'state_tax_edd': 'State Tax', 
            'date_pay_settle': 'Payment date', 
            '941_payment_amount': '941', 
            'EDD_payment_amount':'EDD'
            })

        return df


    def save_to_excel(self, file_path, df_new):

        try:
            # Escribir el DataFrame en una nueva hoja            
            df_resultado = self.group_by_weekly(df_new)

            # df_resultado.to_excel(ruta1, index=False, sheet_name="Resumen")
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df_resultado.to_excel(writer, index=False, sheet_name='Resumen')
                df_new.to_excel(writer, index=False, sheet_name='Datos combinados')

            print(f"Datos guardados en la hoja Datos combinados del archivo {file_path}")
            print(f"Datos guardados en la hoja Datos combinados del archivo {file_path}")

        except Exception as e:
            print(f"Error al guardar los datos en el archivo Excel: {e}")
        
        self.crossamounts(file_path)
        headers = ["Company","Check date","Federal Tax","State Tax","Payment date","941",'EDD', 'Balance 941', 'Balance EDD']
        self.format_excel_headers(file_path, headers)

    def translate_month(self, month):
        return months_translator.get(month, month)
    
    def get_month_number(self, month): 
        return months_numbers.get(month, "Mes desconocido")
    
