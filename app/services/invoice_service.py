from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.invoice import Invoice, InvoiceItem
from app.repositories.invoice_repository import InvoiceRepository
from app.services.accounting_service import AccountingService

class InvoiceService:
    def __init__(self, session: Session):
        self.session = session
        self.invoice_repo = InvoiceRepository(session)
        self.accounting = AccountingService(session)

    def create_invoice(self, customer_id: int, items_data: list,
                       report_id: int = None, discount: Decimal = Decimal("0.00"),
                       tax: Decimal = Decimal("0.00"), notes: str = "") -> Invoice:
        inv_num = self.invoice_repo.get_next_invoice_number()

        invoice = Invoice(
            invoice_number=inv_num,
            customer_id=customer_id,
            report_id=report_id,
            discount=discount,
            tax=tax,
            total_amount=Decimal("0.00"),
            paid_amount=Decimal("0.00"),
            payment_status="تسویه‌نشده",
            notes=notes
        )
        self.invoice_repo.create(invoice)
        self.session.flush()

        subtotal = Decimal("0.00")
        for idx, item in enumerate(items_data):
            u_price = Decimal(str(item.get("unit_price", 0.0)))
            qty = int(item.get("quantity", 1))
            tot = u_price * qty
            subtotal += tot

            inv_item = InvoiceItem(
                invoice_id=invoice.id,
                item_name=item.get("item_name"),
                quantity=qty,
                unit_price=u_price,
                total_price=tot
            )
            self.session.add(inv_item)

        final_total = subtotal - discount + tax
        if final_total < 0:
            final_total = Decimal("0.00")

        invoice.total_amount = final_total
        self.session.flush()

        self.accounting.post_transaction(
            customer_id=customer_id,
            transaction_type="Sales invoice",
            debit_amount=final_total,
            credit_amount=Decimal("0.00"),
            description=f"ثبت فاکتور فروش شماره {inv_num}",
            invoice_id=invoice.id,
            report_id=report_id
        )

        return invoice
