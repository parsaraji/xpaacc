import pytest
from app.document_processing.confidence import ConfidenceCalculator

def test_confidence_calculator():
    data = {
        "patient_name": "بیمار تستی",
        "sample_id": "SMP-900",
        "test_date": "2026/11/01",
        "tests": [
            {"test_name": "SGPT", "value": "16.1", "unit": "U/L"}
        ]
    }
    score = ConfidenceCalculator.calculate_confidence(data)
    assert score == 100.0

    # No tests
    data_no_tests = {
        "patient_name": "بیمار تستی",
        "sample_id": "SMP-900",
        "test_date": "2026/11/01",
        "tests": []
    }
    score_no_tests = ConfidenceCalculator.calculate_confidence(data_no_tests)
    assert score_no_tests < 100.0
