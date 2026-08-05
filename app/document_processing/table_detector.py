import re
from typing import List, Dict, Any

class TableDetector:
    def __init__(self):
        pass

    def reconstruct_lab_table(self, lines: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        reconstructed_rows = []
        unit_pattern = re.compile(r'^(U/L|g/dL|10\^3/uL|mg/dL|%|mmol/L|g/l|u/l|normal|high|low|positive|negative)$', re.IGNORECASE)
        number_pattern = re.compile(r'^([<>]?[0-9]+(\.[0-9]+)?|Trace|Positive|Negative)$', re.IGNORECASE)

        for line in lines:
            line_text = " ".join([w["text"] for w in line])
            if "Patient:" in line_text or "Test Date:" in line_text or "Send Date:" in line_text or "Print Date:" in line_text:
                continue

            if len(line) >= 3:
                test_name = line[0]["text"]
                texts = [w["text"] for w in line]

                candidate_val = texts[1]
                candidate_unit = texts[2] if len(texts) > 2 else ""
                candidate_status = texts[3] if len(texts) > 3 else "Normal"

                if number_pattern.match(candidate_val) or unit_pattern.match(candidate_unit):
                    reconstructed_rows.append({
                        "test_name": test_name,
                        "full_name": "",
                        "value": candidate_val,
                        "unit": candidate_unit,
                        "result_status": candidate_status,
                        "remark": "",
                        "reference": ""
                    })

        return reconstructed_rows
