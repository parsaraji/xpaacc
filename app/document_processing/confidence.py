class ConfidenceCalculator:
    @staticmethod
    def calculate_confidence(extracted_data: dict) -> float:
        score = 100.0

        if not extracted_data.get("patient_name"):
            score -= 15.0
        if not extracted_data.get("sample_id"):
            score -= 10.0
        if not extracted_data.get("test_date"):
            score -= 10.0

        tests = extracted_data.get("tests", [])
        if not tests:
            score -= 25.0
        else:
            for t in tests:
                val = t.get("value", "")
                if not val or val.strip() == "":
                    score -= 5.0

        return max(0.0, min(100.0, score))
