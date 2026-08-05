from decimal import Decimal
import datetime
from sqlalchemy.orm import Session
from app.models.transaction import FinancialTransaction
from app.models.customer import Customer
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.customer_repository import CustomerRepository

class AccountingService:
    def __init__(self, session: Session):
        self.session = session
        self.tx_repo = TransactionRepository(session)
        self.cust_repo = CustomerRepository(session)

    def calculate_running_balances(self, customer_id: int):
        customer = self.cust_repo.get_by_id(customer_id)
        if not customer:
            return

        txs = self.tx_repo.get_by_customer_id(customer_id)

        running = Decimal("0.00")

        for tx in txs:
            if tx.status == "لغوشده":
                continue
            debit = tx.debit_amount or Decimal("0.00")
            credit = tx.credit_amount or Decimal("0.00")
            running += (debit - credit)
            tx.running_balance = running

        customer.current_balance = running
        self.session.flush()

    def post_transaction(self, customer_id: int, transaction_type: str,
                         debit_amount: Decimal, credit_amount: Decimal,
                         description: str = "", reference_number: str = "",
                         payment_method: str = None, invoice_id: int = None,
                         report_id: int = None, notes: str = "") -> FinancialTransaction:
        if debit_amount < 0 or credit_amount < 0:
            raise ValueError("مبالغ نباید منفی باشند.")
        if debit_amount == 0 and credit_amount == 0:
            raise ValueError("مبلغ بدهکار و بستانکار نمی‌تواند هم‌زمان صفر باشد.")

        tx_num = self.tx_repo.get_next_transaction_number()

        tx = FinancialTransaction(
            transaction_number=tx_num,
            customer_id=customer_id,
            transaction_type=transaction_type,
            debit_amount=debit_amount,
            credit_amount=credit_amount,
            description=description,
            reference_number=reference_number,
            payment_method=payment_method,
            invoice_id=invoice_id,
            report_id=report_id,
            notes=notes,
            status="ثبت‌شده"
        )
        self.tx_repo.create(tx)
        self.session.flush()

        self.calculate_running_balances(customer_id)
        return tx

    def reverse_transaction(self, transaction_id: int, reason: str = "") -> FinancialTransaction:
        orig_tx = self.tx_repo.get_by_id(transaction_id)
        if not orig_tx:
            raise ValueError("تراکنش یافت نشد.")
        if orig_tx.status == "لغوشده":
            raise ValueError("این تراکنش قبلاً لغو شده است.")

        orig_tx.status = "لغوشده"

        rev_num = self.tx_repo.get_next_transaction_number()
        rev_tx = FinancialTransaction(
            transaction_number=rev_num,
            customer_id=orig_tx.customer_id,
            transaction_type="Reversal",
            debit_amount=orig_tx.credit_amount,
            credit_amount=orig_tx.debit_amount,
            description=f"برگشت تراکنش {orig_tx.transaction_number} - علت: {reason}",
            reversal_transaction_id=orig_tx.id,
            status="ثبت‌شده"
        )
        self.tx_repo.create(rev_tx)
        self.session.flush()

        self.calculate_running_balances(orig_tx.customer_id)
        return rev_tx
