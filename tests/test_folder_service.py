import os
import tempfile
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from services.folder_service import FolderProcessor
import fitz  # PyMuPDF
from PIL import Image

# === FUNCIONES AUXILIARES ===

def create_test_pdf(path, text="Texto de prueba para OCR"):
    """
    Crea un archivo PDF de prueba con texto en su interior.
    """
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()

# === PRUEBAS UNITARIAS ===

def test_translate_month():
    processor = FolderProcessor("output", "output.xlsx")
    assert processor.translate_month("January") == "Enero"
    assert processor.translate_month("Noviembre") == "November"
    assert processor.translate_month("InvalidMonth") == "InvalidMonth"

def test_get_month_number():
    processor = FolderProcessor("output", "output.xlsx")
    assert processor.get_month_number("January") == 1
    assert processor.get_month_number("Noviembre") == 11
    assert processor.get_month_number("InvalidMonth") == "Mes desconocido"

def test_get_target_path():
    processor = FolderProcessor("output", "output.xlsx")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear estructura de carpetas simulada
        client_folder = os.path.join(temp_dir, "Client1")
        os.makedirs(os.path.join(client_folder, "Payroll 2024", "11 - November"), exist_ok=True)
        
        # Verificar que encuentra la ruta correcta
        target_path = processor._get_target_path(client_folder, "2024", "November", 11)
        assert target_path is not None
        assert "11 - November" in target_path

def test_get_target_path_with_ambiguous_names():
    processor = FolderProcessor("output", "output.xlsx")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear estructura de carpetas simulada
        client_folder = os.path.join(temp_dir, "Client1")
        ambiguous_path = os.path.join(client_folder, "Payroll 2024", "11-November-Test")
        os.makedirs(ambiguous_path, exist_ok=True)
        
        # Validar que no se selecciona la carpeta con nombre ambiguo
        target_path = processor._get_target_path(client_folder, "2024", "November", 11)
        assert target_path is None

def test_process_weekly_files():
    processor = FolderProcessor("output", "output.xlsx")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear PDF válido
        pdf_path = os.path.join(temp_dir, "test_941.pdf")
        create_test_pdf(pdf_path, "Texto de prueba 941")
        
        # Mockear OCR y manejo de datos
        with patch.object(processor, "process_file_with_ocr", return_value="Texto de prueba 941") as mock_ocr, \
             patch.object(processor, "handle_extracted_data", return_value=pd.DataFrame({"tipo_archivo": ["941"], "Name": ["Empresa A"]})) as mock_handle:
            
            df = processor.process_weekly_files(temp_dir, 2024, "November", 1, 0)
            
            assert len(df) == 1
            assert df.iloc[0]["Name"] == "Empresa A"
            mock_ocr.assert_called_once()
            mock_handle.assert_called_once()

def test_process_weekly_files_invalid_files():
    processor = FolderProcessor("output", "output.xlsx")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear archivos no válidos
        invalid_pdf = os.path.join(temp_dir, "invalid_file.txt")
        with open(invalid_pdf, "w") as f:
            f.write("Not a PDF")
        
        valid_pdf = os.path.join(temp_dir, "valid_941.pdf")
        create_test_pdf(valid_pdf, "Texto válido 941")
        
        with patch.object(processor, "process_file_with_ocr", return_value="Texto válido 941") as mock_ocr, \
             patch.object(processor, "handle_extracted_data", return_value=pd.DataFrame({"tipo_archivo": ["941"], "Name": ["Empresa A"]})) as mock_handle:
            
            df = processor.process_weekly_files(temp_dir, 2024, "November", 2, 0)
            
            assert len(df) == 1
            assert df.iloc[0]["Name"] == "Empresa A"
            mock_ocr.assert_called_once()
            mock_handle.assert_called_once()

def test_process_file_with_ocr():
    processor = FolderProcessor("output", "output.xlsx")
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        create_test_pdf(temp_pdf.name, "Texto OCR de prueba")
        extracted_text = processor.process_file_with_ocr(temp_pdf.name)
        assert "Texto OCR de prueba" in extracted_text

def test_process_file_with_ocr_error():
    processor = FolderProcessor("output", "output.xlsx")
    
    with patch("fitz.open", side_effect=Exception("Simulated PDF error")):
        extracted_text = processor.process_file_with_ocr("fake_path.pdf")
        assert extracted_text == ""

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
    
    # Leer y validar datos
    saved_df = pd.read_excel(output_path, sheet_name="Resumen")
    assert len(saved_df) == 2
    assert "Company" in saved_df.columns

def test_handle_extracted_data():
    processor = FolderProcessor("output", "output.xlsx")
    
    # Simular archivo PDF
    data = processor.handle_extracted_data(
        "2024-11-15_941.pdf",
        "Texto de prueba para 941",
        "Cliente1",
        "November",
        2024
    )
    
    assert not data.empty
    assert data.iloc[0]["tipo_archivo"] == "941"
    assert data.iloc[0]["carpeta_cliente"] == "Cliente1"

def test_process():
    processor = FolderProcessor("output", "output.xlsx")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear estructura de carpetas simulada
        client_folder = os.path.join(temp_dir, "Client1", "Payroll 2024", "11 - November")
        os.makedirs(client_folder, exist_ok=True)
        pdf_path = os.path.join(client_folder, "test_941.pdf")
        create_test_pdf(pdf_path, "Texto OCR de prueba")

        # Simular DataFrame de salida
        mock_df = pd.DataFrame({
            "tipo_archivo": ["941"],
            "fecha_pdf": ["2024-11-15"],
            "Name": ["Empresa A"],
            "federal_tax_941": ["1000.00"],
            "state_tax_edd": ["200.00"],
            "941_payment_amount": ["800.00"],
            "EDD_payment_amount": ["150.00"],
            "account_number": ["123456"],
            "date_pay_settle": ["2024-11-20"],
            "carpeta_cliente": ["Client1"]
        })

        # Mockear funciones internas
        with patch.object(processor, "process_weekly_files", return_value=mock_df) as mock_weekly, \
             patch.object(processor, "save_to_excel") as mock_save:
            
            # Ejecutar el proceso
            processor.process(temp_dir, 2024, "November")

            # Verificar que se llamaron las funciones internas
            mock_weekly.assert_called_once()
            mock_save.assert_called_once_with(
                os.path.join(processor.folder_output_ejecutable_unificado, processor.output_file),
                processor.prepare_data(mock_df)
            )

            # Validar que el DataFrame tiene las columnas esperadas
            assert not mock_df.empty
            assert "tipo_archivo" in mock_df.columns
            assert "federal_tax_941" in mock_df.columns
            assert "state_tax_edd" in mock_df.columns


def test_validate_inputs_valid():
    processor = FolderProcessor("output", "output.xlsx")
    with tempfile.TemporaryDirectory() as temp_dir:
        processor.validate_inputs(temp_dir, 2024, "January")

def test_validate_inputs_invalid_folder():
    processor = FolderProcessor("output", "output.xlsx")
    with pytest.raises(FileNotFoundError):
        processor.validate_inputs("/invalid/folder", 2024, "January")

def test_validate_inputs_invalid_year():
    processor = FolderProcessor("output", "output.xlsx")
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(ValueError):
            processor.validate_inputs(temp_dir, 1800, "January")

def test_validate_inputs_invalid_month():
    processor = FolderProcessor("output", "output.xlsx")
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(ValueError):
            processor.validate_inputs(temp_dir, 2024, "InvalidMonth")
