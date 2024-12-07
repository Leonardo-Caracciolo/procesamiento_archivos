import pytest
from procesamiento_archivos.spreadsheet_processor import process_excel
from exceptions import ExcelProcessingError

def test_missing_columns():
    with pytest.raises(ExcelProcessingError, match="no tiene las columnas requeridas"):
        process_excel("test_files/missing_columns.xlsx")
