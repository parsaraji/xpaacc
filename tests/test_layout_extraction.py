import pytest
from app.document_processing.layout_extractor import LayoutExtractor
from app.document_processing.table_detector import TableDetector
from app.document_processing.template_engine import TemplateEngine

def test_layout_and_table_reconstruction():
    # Simulate coordinate words like layout coordinates inside visual document
    # "Patient: 3- 1:5" at y0 = 100
    words = [
        {"x0": 10.0, "y0": 100.0, "x1": 50.0, "y1": 115.0, "text": "Patient:"},
        {"x0": 55.0, "y0": 100.0, "x1": 100.0, "y1": 115.0, "text": "3-"},
        {"x0": 105.0, "y0": 100.0, "x1": 150.0, "y1": 115.0, "text": "1:5"},

        # Row 1: "SGPT    16.1    U/L    Normal" at y0 = 200
        {"x0": 10.0, "y0": 200.0, "x1": 50.0, "y1": 215.0, "text": "SGPT"},
        {"x0": 100.0, "y0": 200.0, "x1": 130.0, "y1": 215.0, "text": "16.1"},
        {"x0": 180.0, "y0": 200.0, "x1": 210.0, "y1": 215.0, "text": "U/L"},
        {"x0": 250.0, "y0": 200.0, "x1": 290.0, "y1": 215.0, "text": "Normal"},
    ]

    extractor = LayoutExtractor()
    lines = extractor.group_words_into_lines(words)

    assert len(lines) == 2

    text_lines = extractor.get_lines_as_text(lines)
    assert "Patient: 3- 1:5" in text_lines[0]
    assert "SGPT 16.1 U/L Normal" in text_lines[1]

    detector = TableDetector()
    rows = detector.reconstruct_lab_table(lines)
    assert len(rows) == 1
    assert rows[0]["test_name"] == "SGPT"
    assert rows[0]["value"] == "16.1"
    assert rows[0]["unit"] == "U/L"
    assert rows[0]["result_status"] == "Normal"
