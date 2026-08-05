from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from app.config import FONT_NAME
from app.document_processing.document_loader import DocumentLoader
from app.document_processing.page_renderer import PageRenderer
from app.document_processing.layout_extractor import LayoutExtractor
from app.document_processing.template_engine import TemplateEngine
import os

class DocumentViewer(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.doc = None
        self.current_page_idx = 0
        self.zoom_factor = 1.0
        self.filepath = ""

        self.loader = DocumentLoader()
        self.renderer = PageRenderer(dpi=150)
        self.extractor = LayoutExtractor()
        self.engine = TemplateEngine()
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.title_lbl = QLabel("نمایشگر سند آزمایشگاه")
        self.title_lbl.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        self.title_lbl.setStyleSheet("color: #a62626;")
        toolbar.addWidget(self.title_lbl)

        prev_btn = QPushButton("صفحه قبلی")
        prev_btn.setStyleSheet("background-color: #f3f3f3; color: #4b5563; border: 1px solid #e0e0e0;")
        prev_btn.clicked.connect(self.prev_page)
        toolbar.addWidget(prev_btn)

        self.page_num_lbl = QLabel("صفحه ۰ از ۰")
        toolbar.addWidget(self.page_num_lbl)

        next_btn = QPushButton("صفحه بعدی")
        next_btn.setStyleSheet("background-color: #f3f3f3; color: #4b5563; border: 1px solid #e0e0e0;")
        next_btn.clicked.connect(self.next_page)
        toolbar.addWidget(next_btn)

        zoom_in_btn = QPushButton("بزرگنمایی (+)")
        zoom_in_btn.setStyleSheet("background-color: #f3f3f3; color: #4b5563; border: 1px solid #e0e0e0;")
        zoom_in_btn.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in_btn)

        zoom_out_btn = QPushButton("کوچکنمایی (-)")
        zoom_out_btn.setStyleSheet("background-color: #f3f3f3; color: #4b5563; border: 1px solid #e0e0e0;")
        zoom_out_btn.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out_btn)

        toolbar.addStretch()

        process_btn = QPushButton("شروع استخراج هوشمند")
        process_btn.setStyleSheet("background-color: #a62626; color: white; font-weight: bold; padding: 6px 12px;")
        process_btn.clicked.connect(self.start_extraction)
        toolbar.addWidget(process_btn)

        layout.addLayout(toolbar)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("background-color: #ffffff;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.canvas_lbl = QLabel()
        self.canvas_lbl.setAlignment(Qt.AlignCenter)
        self.canvas_lbl.setStyleSheet("background-color: #f3f4f6; border: 1px solid #e0e0e0;")
        scroll.setWidget(self.canvas_lbl)
        splitter.addWidget(scroll)

        text_panel = QFrame()
        text_panel.setStyleSheet("background-color: #ffffff; border: 1px solid #e0e0e0;")
        text_layout = QVBoxLayout(text_panel)

        text_title = QLabel("متن استخراج شده از سند")
        text_title.setFont(QFont(FONT_NAME, 11, QFont.Bold))
        text_title.setStyleSheet("color: #a62626;")
        text_layout.addWidget(text_title)

        self.raw_text_lbl = QLabel("متن جهت استخراج آماده است.")
        self.raw_text_lbl.setWordWrap(True)
        self.raw_text_lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.raw_text_lbl.setStyleSheet("background-color: #f9fafb; padding: 10px; border-radius: 4px; border: 1px solid #e0e0e0;")

        text_scroll = QScrollArea()
        text_scroll.setWidgetResizable(True)
        text_scroll.setWidget(self.raw_text_lbl)
        text_layout.addWidget(text_scroll)

        splitter.addWidget(text_panel)
        splitter.setSizes([600, 300])

        layout.addWidget(splitter)

    def load_file(self, filepath: str):
        self.filepath = filepath
        self.doc = self.loader.open_document(filepath)
        self.current_page_idx = 0
        self.title_lbl.setText(f"سند: {os.path.basename(filepath)}")
        self.render_current_page()

    def render_current_page(self):
        if not self.doc:
            return

        page = self.doc[self.current_page_idx]
        pixmap = self.renderer.render_page_to_image(page, zoom=self.zoom_factor)
        self.canvas_lbl.setPixmap(pixmap)

        self.page_num_lbl.setText(f"صفحه {self.current_page_idx + 1} از {len(self.doc)}")

        words = self.extractor.extract_structured_words(page)
        lines = self.extractor.group_words_into_lines(words)
        text_lines = self.extractor.get_lines_as_text(lines)
        self.raw_text_lbl.setText("\n".join(text_lines))

    def prev_page(self):
        if self.doc and self.current_page_idx > 0:
            self.current_page_idx -= 1
            self.render_current_page()

    def next_page(self):
        if self.doc and self.current_page_idx < len(self.doc) - 1:
            self.current_page_idx += 1
            self.render_current_page()

    def zoom_in(self):
        self.zoom_factor += 0.15
        self.render_current_page()

    def zoom_out(self):
        if self.zoom_factor > 0.4:
            self.zoom_factor -= 0.15
            self.render_current_page()

    def start_extraction(self):
        if not self.doc:
            return

        page = self.doc[self.current_page_idx]
        words = self.extractor.extract_structured_words(page)
        extracted_data = self.engine.extract_all(words)
        extracted_data["original_filename"] = os.path.basename(self.filepath)

        self.main_window.extraction_review_page.set_review_data(extracted_data)
        self.main_window.navigate_to_page(15)
