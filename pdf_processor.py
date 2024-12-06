import fitz
from exceptions import PDFProcessingError

def process_pdf(file_path):
    """
    Procesa un archivo PDF, manejando casos de contraseñas y PDFs escaneados.
    """
    if not file_path:
        print("No se seleccionó ningún archivo.")
        return

    try:
        doc = fitz.open(file_path)

        # Detectar si el PDF está protegido con contraseña
        if doc.needs_pass:
            raise PDFProcessingError("El archivo PDF está protegido con contraseña.")

        # Procesar el contenido
        text = ""
        for page in doc:
            text += page.get_text()

        if not text.strip():
            raise PDFProcessingError("El archivo PDF parece ser un escaneo (sin texto extraíble).")

        print("Texto extraído del PDF:")
        print(text)

    except PDFProcessingError as e:
        print(f"Error al procesar el PDF: {e}")
    except Exception as e:
        print(f"Error inesperado al procesar el PDF: {e}")
