import sys
import os
import tempfile
import pytest
import pandas as pd
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.folder_service import FolderProcessor, ErrorLogger
import fitz  # PyMuPDF

# === FUNCIONES AUXILIARES ===

def create_test_pdf(path, text="Texto de prueba para OCR"):
    """
    Crea un archivo PDF de prueba con texto en su interior.
    """
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()  # Asegúrate de cerrar el documento
# === PRUEBAS UNITARIAS ===

def test_get_month_number():
    processor = FolderProcessor("output", "output.xlsx")
    assert processor.get_month_number("January") == 1
    assert processor.get_month_number("Febrero") == 2
    assert processor.get_month_number("InvalidMonth") == "Mes desconocido"

def test_translate_month():
    processor = FolderProcessor("output", "output.xlsx")
    assert processor.translate_month("January") == "Enero"
    assert processor.translate_month("Febrero") == "February"
    assert processor.translate_month("InvalidMonth") == "InvalidMonth"

def test_format_date():
    processor = FolderProcessor("output", "output.xlsx")
    assert processor.format_date("2024-01-15") == "2024-01-15"
    assert processor.format_date("InvalidDate") == "Fecha inválida"

@patch("os.listdir")
@patch("services.folder_service.FolderProcessor.process_file_with_ocr")
@patch("services.folder_service.FolderProcessor.handle_extracted_data")
def test_process_weekly_files(mock_handle_data, mock_ocr, mock_listdir):
    # Configuración de los mocks
    mock_listdir.return_value = ["test_941.pdf", "test_EDD.pdf"]
    mock_ocr.side_effect = ["Texto OCR 941", "Texto OCR EDD"]
    mock_handle_data.side_effect = [
        pd.DataFrame({"tipo_archivo": ["941"], "Name": ["Empresa A"]}),
        pd.DataFrame({"tipo_archivo": ["EDD"], "Name": ["Empresa B"]}),
    ]

    # Ejecución
    processor = FolderProcessor("output", "output.xlsx")
    df = processor.process_weekly_files("/dummy/folder", 2024, "January", 2)

    # Verificaciones
    # 1. Validar que se llamó a `handle_extracted_data` dos veces
    assert mock_handle_data.call_count == 2

    # 2. Validar los argumentos con los que se llamó a `handle_extracted_data`
    expected_calls = [
        (("test_941.pdf", "Texto OCR 941", "/dummy/folder", "January", 2024),),
        (("test_EDD.pdf", "Texto OCR EDD", "/dummy/folder", "January", 2024),),
    ]
    assert mock_handle_data.call_args_list == expected_calls

    # 3. Validar el DataFrame devuelto
    assert len(df) == 2
    assert "Empresa A" in df["Name"].values
    assert "Empresa B" in df["Name"].values


def test_process_file_with_ocr():
    processor = FolderProcessor("output", "output.xlsx")

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        create_test_pdf(temp_pdf.name)
        extracted_text = processor.process_file_with_ocr(temp_pdf.name)
        assert "Texto de prueba" in extracted_text

def test_save_to_excel():
    processor = FolderProcessor("output", "test_output.xlsx")
    df = pd.DataFrame({
        "Company": ["Client1", "Client2"],
        "Check date": ["2024-01-15", "2024-02-15"]
    })

    output_path = os.path.join("output", "test_output.xlsx")
    processor.save_to_excel(output_path, df)

    # Verificar que el archivo fue creado
    assert os.path.exists(output_path)

    # Leer el archivo y validar los datos
    saved_df = pd.read_excel(output_path, sheet_name="Resumen")
    assert len(saved_df) == 2
    assert "Company" in saved_df.columns

def test_error_logging():
    logger = ErrorLogger("output/error_log.json")
    logger.log_error("test_file.pdf", "OCR Error")

    assert len(logger.errors) == 1
    assert logger.errors[0]["file"] == "test_file.pdf"
    assert logger.errors[0]["error"] == "OCR Error"

    logger.save_log()
    assert os.path.exists("output/error_log.json")

# === PRUEBAS DE VALIDACIÓN ===

def test_validate_inputs_valid():
    processor = FolderProcessor("output", "output.xlsx")
    parent_folder = tempfile.mkdtemp()
    os.makedirs(parent_folder, exist_ok=True)
    processor.validate_inputs(parent_folder, 2024, "January")

def test_validate_inputs_invalid_folder():
    processor = FolderProcessor("output", "output.xlsx")
    with pytest.raises(FileNotFoundError):
        processor.validate_inputs("/invalid/folder", 2024, "January")

def test_validate_inputs_invalid_year():
    processor = FolderProcessor("output", "output.xlsx")
    temp_folder = tempfile.mkdtemp()
    with pytest.raises(ValueError):
        processor.validate_inputs(temp_folder, 1900, "January")
        
        
import tempfile

def test_validate_inputs_invalid_month():
    processor = FolderProcessor("output", "output.xlsx")
    with tempfile.TemporaryDirectory() as temp_folder:  # Crear un directorio temporal
        with pytest.raises(ValueError):
            processor.validate_inputs(temp_folder, 2024, "InvalidMonth")
