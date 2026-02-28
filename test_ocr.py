from app.services.ocr_engine import OCREngine

path = r"C:\Users\rvlgs\OneDrive\Pictures\PdfImage.png"
print(OCREngine.extract_text(path))

