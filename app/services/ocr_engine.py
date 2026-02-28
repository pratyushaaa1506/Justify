from PIL import Image
import cv2
import numpy as np
import os
from pdf2image import convert_from_path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Optional: Allow user to set Tesseract path via env var
TESSERACT_CMD = os.getenv("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class OCREngine:
    @staticmethod
    def extract_text(image_input) -> str:
        """
        Accepts either a file path (str), bytes, or a file-like object.
        """
        try:
            # If input is a string, treat as file path
            if isinstance(image_input, str):
                ext = os.path.splitext(image_input)[1].lower()
                if ext == ".pdf":
                    pages = convert_from_path(image_input)
                    texts = []
                    for page in pages:
                        text = OCREngine._ocr_pil_image(page)
                        if text:
                            texts.append(text)
                    return "\n".join(texts).strip()
                else:
                    img = Image.open(image_input)
                    return OCREngine._ocr_pil_image(img)
            # If input is bytes or file-like, try to open as image
            else:
                # If UploadFile, get .file
                if hasattr(image_input, "file"):
                    image_input = image_input.file
                # If PDF, not supported for bytes/file-like (could add support)
                # For now, treat as image
                img = Image.open(image_input)
                return OCREngine._ocr_pil_image(img)
        except Exception:
            return ""

    @staticmethod
    def _ocr_pil_image(img: Image.Image) -> str:
        try:
            # Convert to OpenCV format
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            # Grayscale
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            # Thresholding
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # Back to PIL
            proc_img = Image.fromarray(thresh)
            text = pytesseract.image_to_string(proc_img)
            return text.strip()
        except Exception:
            
            try:
                return pytesseract.image_to_string(img).strip()
            except Exception:
                return ""
