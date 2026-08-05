from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PdfExporter:
    def __init__(self):
        pass

    def _sanitize_text(self, text: str) -> str:
        if not text:
            return ""
        mapping = {
            'ع': 'A', 'ل': 'l', 'ی': 'i', 'ر': 'r', 'ض': 'z', 'ا': 'a',
            'ر': 'r', 'ض': 'z', 'ا': 'a', 'ی': 'i', ' ': ' ',
            'خ': 'Kh', 'ا': 'a', 'ن': 'n', 'م': 'm', 'و': 'o', 'د': 'd'
        }
        sanitized = []
        for char in text:
            if ord(char) < 128:
                sanitized.append(char)
            else:
                sanitized.append(mapping.get(char, '?'))
        return "".join(sanitized)

    def export_customer_statement(self, customer_name: str, transactions: list, filepath: str):
        """
        Generates a professional single PDF statement.
        """
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            name='TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            alignment=1
        )

        safe_name = self._sanitize_text(customer_name)

        story.append(Paragraph("Laboratory Report Statement", title_style))
        story.append(Spacer(1, 15))

        body_style = ParagraphStyle(
            name='BodyStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14
        )
        story.append(Paragraph(f"Customer Name: {safe_name}", body_style))
        story.append(Spacer(1, 15))

        table_data = [["Tx Number", "Type", "Debit", "Credit", "Balance"]]
        for tx in transactions:
            table_data.append([
                self._sanitize_text(tx.transaction_number),
                self._sanitize_text(tx.transaction_type),
                f"{tx.debit_amount:,.2f}",
                f"{tx.credit_amount:,.2f}",
                f"{tx.running_balance:,.2f}"
            ])

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.teal),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('GRID', (0,0), (-1,-1), 1, colors.grey)
        ]))
        story.append(t)

        doc.build(story)

    def export_group_statements(self, customer_statement_list: list, filepath: str):
        """
        Generates a combined group PDF statement for multiple customers sequentially.
        customer_statement_list is a list of dicts: [{'customer_name': '...', 'transactions': [...]}]
        """
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            name='GroupTitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            alignment=1,
            textColor=colors.teal
        )
        story.append(Paragraph("Group Laboratory Account Statements", title_style))
        story.append(Spacer(1, 20))

        body_style = ParagraphStyle(
            name='GroupBodyStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14
        )

        for entry in customer_statement_list:
            c_name = self._sanitize_text(entry['customer_name'])
            txs = entry['transactions']

            story.append(Paragraph(f"Customer Account Ledger Statement: {c_name}", body_style))
            story.append(Spacer(1, 8))

            table_data = [["Tx Number", "Type", "Debit", "Credit", "Balance"]]
            for tx in txs:
                table_data.append([
                    self._sanitize_text(tx.transaction_number),
                    self._sanitize_text(tx.transaction_type),
                    f"{tx.debit_amount:,.2f}",
                    f"{tx.credit_amount:,.2f}",
                    f"{tx.running_balance:,.2f}"
                ])

            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 4),
                ('GRID', (0,0), (-1,-1), 1, colors.lightgrey)
            ]))
            story.append(t)
            story.append(Spacer(1, 25))

        doc.build(story)
