import os
import fitz
from typing import List, Optional

class DocumentLoader:
    def __init__(self):
        pass

    def open_document(self, filepath: str) -> fitz.Document:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"فایل در مسیر مشخص شده یافت نشد: {filepath}")
        try:
            doc = fitz.open(filepath)
            return doc
        except Exception as e:
            raise ValueError(f"خطا در باز کردن فایل: {str(e)}")
