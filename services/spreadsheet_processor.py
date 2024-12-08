import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import os


class ExcelProcessor:
    def process(self, df: pd.DataFrame, header_row: int, data_row: int, output_path: str):
        """
        Procesa un DataFrame, escribiéndolo en una hoja de Excel.
        - Encabezados: Calibri 20, alineación inferior, fondo gris, color de letra negro.
        - Datos: Calibri 12, alineación centrada.
        - Ajusta automáticamente el ancho de las columnas.
        """
        try:
            # Crear un nuevo archivo Excel
            wb = Workbook()
            ws = wb.active
            ws.title = "Data"

            # Estilo de los encabezados
            header_font = Font(name="Calibri", size=20, color="000000", bold=True)
            header_fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")  # Gris
            header_alignment = Alignment(horizontal="center", vertical="bottom")

            # Escribir encabezados con formato
            for col_num, column_name in enumerate(df.columns, start=1):
                cell = ws.cell(row=header_row, column=col_num, value=column_name)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment

            # Escribir datos del DataFrame a partir de la fila indicada
            for row in dataframe_to_rows(df, index=False, header=False):
                ws.append(row)

            # Aplicar estilo a las celdas de datos
            for row in ws.iter_rows(min_row=data_row, max_row=ws.max_row, min_col=1, max_col=len(df.columns)):
                for cell in row:
                    cell.font = Font(name="Calibri", size=12)  # Fuente Calibri 12
                    cell.alignment = Alignment(horizontal="center", vertical="center")  # Centrado

            # Ajustar automáticamente el ancho de las columnas
            self._adjust_column_widths(ws, df.columns)

            # Guardar el archivo Excel en la ruta especificada
            wb.save(output_path)
            print(f"Archivo Excel guardado exitosamente en: {output_path}")

        except Exception as e:
            print(f"Error al procesar el archivo Excel: {e}")


    def _adjust_column_widths(self, sheet, headers):
        """
        Ajusta el ancho de las columnas automáticamente basado en el contenido más largo (incluye encabezados y celdas).
        """
        for col_idx, column_cells in enumerate(sheet.columns, start=1):
            max_length = 0
            column = column_cells[0].column_letter  # Obtiene la letra de la columna
            for cell in column_cells:
                try:
                    if cell.value:
                        # Comparar longitud de texto en las celdas
                        max_length = max(max_length, len(str(cell.value)))
                except Exception as e:
                    print(f"Error al calcular el ancho: {e}")

            # Comparar con el encabezado explícitamente
            max_length = max(max_length, len(headers[col_idx - 1]))

            # Ajustar ancho con un margen adicional
            sheet.column_dimensions[column].width = max_length + 2


# Ejemplo de uso
if __name__ == "__main__":
    # Crear un ejemplo de DataFrame
    data = {
        "Company": ["Company A", "Company B"],
        "Check Date": ["2024-12-01", "2024-12-02"],
        "Federal Tax Amount": [1000, 2000],  # Encabezado más largo para prueba
        "State Tax": [300, 400],
        "Additional Comments": ["This is a long comment.", "Short comment."],
    }
    df = pd.DataFrame(data)

    # Ruta de salida en la carpeta del script
    # output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.xlsx")
    output_path = r"L:\Procesamiento_PDF\procesamiento_archivos\Data\Inputs\salida.xlsx"
    # Procesar el DataFrame y guardar el archivo Excel
    processor = ExcelProcessor()
    processor.process(df, header_row=1, data_row=2, output_path=output_path)
