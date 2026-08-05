import openpyxl
from typing import List
from app.models.transaction import FinancialTransaction

class ExcelExporter:
    def __init__(self):
        pass

    def export_transactions(self, transactions: List[FinancialTransaction], filepath: str):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "صورتحساب مالی"

        # RTL Sheet direction
        ws.views.sheetView[0].showGridLines = True

        # Add Headers
        headers = ["شناسه تراکنش", "تاریخ تراکنش", "نوع تراکنش", "شرح تراکنش", "بدهکار (ریال/تومان)", "بستانکار (ریال/تومان)", "مانده"]
        ws.append(headers)

        for tx in transactions:
            ws.append([
                tx.transaction_number,
                tx.transaction_date.strftime("%Y/%m/%d %H:%M:%S") if tx.transaction_date else "",
                tx.transaction_type,
                tx.description or "",
                float(tx.debit_amount or 0.0),
                float(tx.credit_amount or 0.0),
                float(tx.running_balance or 0.0)
            ])

        wb.save(filepath)
