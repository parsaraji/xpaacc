import fitz
from typing import List, Dict, Any

class LayoutExtractor:
    def __init__(self, y_tolerance: float = 3.0):
        self.y_tolerance = y_tolerance

    def extract_structured_words(self, page: fitz.Page) -> List[Dict[str, Any]]:
        words_list = []
        raw_words = page.get_text("words")
        for w in raw_words:
            words_list.append({
                "x0": w[0],
                "y0": w[1],
                "x1": w[2],
                "y1": w[3],
                "text": w[4].strip(),
                "block_no": w[5],
                "line_no": w[6],
                "word_no": w[7]
            })
        return words_list

    def group_words_into_lines(self, words: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        if not words:
            return []

        sorted_words = sorted(words, key=lambda w: (w["y0"], w["x0"]))
        lines = []
        current_line = [sorted_words[0]]

        for w in sorted_words[1:]:
            last_w = current_line[-1]
            if abs(w["y0"] - last_w["y0"]) <= self.y_tolerance:
                current_line.append(w)
            else:
                current_line.sort(key=lambda item: item["x0"])
                lines.append(current_line)
                current_line = [w]

        if current_line:
            current_line.sort(key=lambda item: item["x0"])
            lines.append(current_line)

        return lines

    def get_lines_as_text(self, lines: List[List[Dict[str, Any]]]) -> List[str]:
        text_lines = []
        for line in lines:
            line_text = " ".join([w["text"] for w in line])
            text_lines.append(line_text)
        return text_lines
