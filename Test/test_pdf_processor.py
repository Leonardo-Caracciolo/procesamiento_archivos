import pytest
from pdf_processor import process_pdf
from exceptions import PDFProcessingError

def test_pdf_with_password():
    with pytest.raises(PDFProcessingError, match="protegido con contraseña"):
        process_pdf("test_files/protected.pdf")

def test_pdf_scan():
    with pytest.raises(PDFProcessingError, match="parece ser un escaneo"):
        process_pdf("test_files/scanned.pdf")
