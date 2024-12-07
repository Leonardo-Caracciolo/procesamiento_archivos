import pytesseract
from pdf2image import convert_from_path

class OCRHandler:
    def is_editable(self, file_path):
        """Determinar si un archivo PDF es editable."""
        try:
            text = pytesseract.image_to_string(convert_from_path(file_path, first_page=1, last_page=1)[0])
            return bool(text.strip())
        except Exception as e:
            print(f"Error al verificar si el archivo es editable: {e}")
            return False

    def apply_ocr(self, file_path):
        """Aplicar OCR a un archivo PDF."""
        images = convert_from_path(file_path)
        extracted_text = ""
        for image in images:
            extracted_text += pytesseract.image_to_string(image)
        print(f"Texto extraído:\n{extracted_text}")
