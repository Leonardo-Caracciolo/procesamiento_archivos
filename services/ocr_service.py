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



    # document = fitz.open(pdfpath)
    # account_number = None

    # for page_num in range(len(document)):
    #     # Extraer la página como imagen
    #     page = document.load_page(page_num)
    #     pix = page.get_pixmap(dpi=300)  # Resolución alta para mejor OCR
    #     img = Image.open(io.BytesIO(pix.tobytes("png")))

    #     # Preprocesar la imagen
    #     img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)  # Escala de grises
    #     img_cv = cv2.fastNlMeansDenoising(img_cv, None, 30, 7, 21)  # Reducción de ruido
    #     , img_cv = cv2.threshold(img_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarización

    #     # Convertir de nuevo a PIL
    #     processed_img = Image.fromarray(img_cv)

    #     # Realizar OCR
    #     ocr_text = pytesseract.image_to_string(processed_img, lang=lang, config='--psm 6')

    #     print(f"Texto extraído de la página {page_num + 1}:\n{ocr_text}")  # Debugging: Ver texto extraído

    #     # Buscar la línea que contiene "Account Number"
    #     for line in ocr_text.split('\n'):
    #         if "Account Number" in line:
    #             # Extraer el texto asociado
    #             match = re.search(r'Account Number[:\s]*([^\n]+)', line, re.IGNORECASE)
    #             if match:
    #                 raw_number = match.group(1).strip()  # Capturar el valor después de "Account Number"

    #                 # Limpiar y reconstruir el formato "XXXX"
    #                 digits = ''.join(filter(str.isdigit, raw_number))  # Extraer solo dígitos
    #                 if len(digits) >= 4:
    #                     account_number = f"{digits[-4:]}"  # Usar los últimos 4 dígitos
    #                 else:
    #                     account_number = raw_number  # Dejar el texto crudo si no es válido
    #                 break
