import cv2
import numpy as np
import pytesseract
from PIL import Image
from typing import Dict, Any, List

class OcrEngine:
    def __init__(self, tesseract_path: str = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def preprocess_image(self, pixmap_data: bytes) -> np.ndarray:
        nparr = np.frombuffer(pixmap_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("تصویر نامعتبر است.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast = clahe.apply(gray)
        thresh = cv2.adaptiveThreshold(
            contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        denoised = cv2.fastNlMeansDenoising(thresh, h=3)
        return denoised

    def run_ocr_on_image(self, pil_image: Image, lang: str = "fas+eng") -> str:
        try:
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(pil_image, lang=lang, config=custom_config)
            return text
        except Exception as e:
            try:
                text = pytesseract.image_to_string(pil_image, lang="eng", config=custom_config)
                return text
            except Exception:
                return f"خطا در پردازش OCR: {str(e)}"
