import re
from typing import Dict, Any, List
from app.document_processing.layout_extractor import LayoutExtractor
from app.document_processing.table_detector import TableDetector

class TemplateEngine:
    def __init__(self):
        self.extractor = LayoutExtractor()
        self.table_detector = TableDetector()

    def parse_document_text(self, text_lines: List[str]) -> Dict[str, Any]:
        data = {
            "patient_name": "",
            "sample_type": "",
            "sample_id": "",
            "priority": "",
            "test_date": "",
            "send_date": "",
            "print_date": ""
        }

        for line in text_lines:
            if "Patient:" in line:
                data["patient_name"] = line.split("Patient:")[1].strip()
            elif "Sample ID:" in line:
                data["sample_id"] = line.split("Sample ID:")[1].strip()
            elif "Sample:" in line:
                data["sample_type"] = line.split("Sample:")[1].strip()
            elif "Priority:" in line:
                data["priority"] = line.split("Priority:")[1].strip()
            elif "Test Date:" in line:
                data["test_date"] = line.split("Test Date:")[1].strip()
            elif "Send Date:" in line:
                data["send_date"] = line.split("Send Date:")[1].strip()
            elif "Print Date:" in line:
                data["print_date"] = line.split("Print Date:")[1].strip()

        return data

    def extract_all(self, page_words: list) -> Dict[str, Any]:
        lines = self.extractor.group_words_into_lines(page_words)
        text_lines = self.extractor.get_lines_as_text(lines)
        metadata = self.parse_document_text(text_lines)
        tests = self.table_detector.reconstruct_lab_table(lines)
        metadata["tests"] = tests
        return metadata
