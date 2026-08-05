import fitz
from PySide6.QtGui import QPixmap, QImage

class PageRenderer:
    def __init__(self, dpi: int = 150):
        self.dpi = dpi

    def render_page_to_image(self, page: fitz.Page, zoom: float = 1.0) -> QPixmap:
        zoom_factor = (self.dpi / 72.0) * zoom
        matrix = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def render_page_thumbnail(self, page: fitz.Page, width: int = 120) -> QPixmap:
        rect = page.rect
        aspect = rect.y1 / rect.x0 if rect.x0 > 0 else 1.41
        height = int(width * aspect)
        matrix = fitz.Matrix(width / rect.x1, height / rect.y1)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)
