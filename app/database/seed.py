import datetime
from decimal import Decimal
from app.database.session import get_db_session
from app.models.customer import Customer
from app.models.transaction import FinancialTransaction
from app.models.invoice import Invoice, InvoiceItem
from app.models.laboratory_report import LaboratoryReport
from app.models.laboratory_test import LaboratoryTestResult
from app.models.extraction_template import ExtractionTemplate
from app.models.lab_test_catalog import LabTestCatalog

def seed_initial_data():
    with get_db_session() as session:
        if session.query(Customer).count() > 0:
            return

        # Seed Lab Test Catalog
        tests_catalog = [
            LabTestCatalog(test_code="T3", full_name="Triiodothyronine", default_unit="ng/mL", reference_range="0.8 - 2.0", default_fee=Decimal("85000.00"), category="Thyroid"),
            LabTestCatalog(test_code="T4", full_name="Thyroxine", default_unit="ug/dL", reference_range="4.5 - 12.0", default_fee=Decimal("95000.00"), category="Thyroid"),
            LabTestCatalog(test_code="TSH", full_name="Thyroid Stimulating Hormone", default_unit="uIU/mL", reference_range="0.4 - 4.0", default_fee=Decimal("110000.00"), category="Thyroid"),
            LabTestCatalog(test_code="SGPT", full_name="Alanine Aminotransferase", default_unit="U/L", reference_range="0 - 45", default_fee=Decimal("45000.00"), category="Liver Enzymes"),
            LabTestCatalog(test_code="SGOT", full_name="Aspartate Aminotransferase", default_unit="U/L", reference_range="0 - 40", default_fee=Decimal("45000.00"), category="Liver Enzymes"),
            LabTestCatalog(test_code="ALP", full_name="Alkaline Phosphatase", default_unit="U/L", reference_range="30 - 120", default_fee=Decimal("50000.00"), category="Liver Enzymes")
        ]
        for t in tests_catalog:
            session.add(t)
        session.flush()

        template = ExtractionTemplate(
            name="قالب آزمایشگاه پیش‌فرض",
            laboratory_name="آزمایشگاه مرکزی رازی",
            width=Decimal("595.00"),
            height=Decimal("842.00")
        )
        session.add(template)
        session.flush()

        customers = [
            Customer(
                customer_code="CUS-000001",
                customer_type="شخص حقیقی",
                first_name="علیرضا",
                last_name="رضایی",
                display_name="علیرضا رضایی",
                mobile="09121111111",
                national_id="1234567890",
                opening_balance=Decimal("50000"),
                opening_balance_type="DEBIT",
                current_balance=Decimal("50000"),
                province="تهران",
                city="تهران",
                address="خیابان آزادی، پلاک ۱۰",
                notes="مشتری دائمی"
            ),
            Customer(
                customer_code="CUS-000002",
                customer_type="شخص حقوقی",
                company_name="شرکت داروسازی پارس",
                display_name="شرکت داروسازی پارس",
                mobile="09122222222",
                national_id="0987654321",
                opening_balance=Decimal("200000"),
                opening_balance_type="CREDIT",
                current_balance=Decimal("-200000"),
                province="البرز",
                city="کرج",
                address="شهرک صنعتی بهارستان"
            )
        ]

        for cust in customers:
            session.add(cust)
        session.flush()

        # Seed Exactly TWO Laboratory Reports
        reports = [
            LaboratoryReport(
                report_number="REP-9001",
                customer_id=customers[0].id,
                patient_name="کاربر شماره ۱",
                sample_id="SMP-100",
                sample_type="Serum",
                test_date="7/11/2026 4:09:57 PM",
                send_date="7/11/2026 4:09:57 PM",
                print_date="7/11/2026 5:00:37 PM",
                original_filename="report_1.xps",
                review_status="تأییدشده"
            ),
            LaboratoryReport(
                report_number="REP-9002",
                customer_id=customers[1].id,
                patient_name="کاربر شماره ۲",
                sample_id="SMP-200",
                sample_type="Plasma",
                test_date="8/11/2026 10:00:00 AM",
                send_date="8/11/2026 11:30:00 AM",
                print_date="8/11/2026 12:00:00 PM",
                original_filename="report_2.xps",
                review_status="جدید"
            )
        ]

        for rep in reports:
            session.add(rep)
        session.flush()

        test_results = [
            LaboratoryTestResult(report_id=reports[0].id, test_name="TSH", value_text="1.25", unit="uIU/mL", result_status="Normal", row_number=1),
            LaboratoryTestResult(report_id=reports[0].id, test_name="T3", value_text="1.1", unit="ng/mL", result_status="Normal", row_number=2),

            LaboratoryTestResult(report_id=reports[1].id, test_name="SGPT", value_text="16.1", unit="U/L", result_status="Normal", row_number=1),
            LaboratoryTestResult(report_id=reports[1].id, test_name="SGOT", value_text="13.2", unit="U/L", result_status="Normal", row_number=2)
        ]

        for tr in test_results:
            session.add(tr)
        session.flush()

        # Seed Exactly TWO Invoices
        invoices = [
            Invoice(
                invoice_number="INV-2026-0001",
                customer_id=customers[0].id,
                report_id=reports[0].id,
                total_amount=Decimal("195000"),
                paid_amount=Decimal("195000"),
                payment_status="تسویه‌شده"
            ),
            Invoice(
                invoice_number="INV-2026-0002",
                customer_id=customers[1].id,
                report_id=reports[1].id,
                total_amount=Decimal("90000"),
                paid_amount=Decimal("90000"),
                payment_status="تسویه‌شده"
            )
        ]

        for inv in invoices:
            session.add(inv)
        session.flush()

        invoice_items = [
            InvoiceItem(invoice_id=invoices[0].id, item_name="هزینه آزمایش T3 & TSH", quantity=1, unit_price=Decimal("195000"), total_price=Decimal("195000")),
            InvoiceItem(invoice_id=invoices[1].id, item_name="هزینه آزمایش SGPT & SGOT", quantity=1, unit_price=Decimal("90000"), total_price=Decimal("90000"))
        ]

        for item in invoice_items:
            session.add(item)
        session.flush()

        transactions = [
            FinancialTransaction(
                transaction_number="TXN-100001",
                customer_id=customers[0].id,
                transaction_type="Opening balance",
                debit_amount=Decimal("50000"),
                running_balance=Decimal("50000"),
                description="مانده ابتدای دوره"
            ),
            FinancialTransaction(
                transaction_number="TXN-100002",
                customer_id=customers[0].id,
                transaction_type="Sales invoice",
                debit_amount=Decimal("195000"),
                running_balance=Decimal("245000"),
                invoice_id=invoices[0].id,
                description="فاکتور آزمایش شماره INV-2026-0001"
            ),
            FinancialTransaction(
                transaction_number="TXN-100003",
                customer_id=customers[0].id,
                transaction_type="Customer payment received",
                credit_amount=Decimal("195000"),
                running_balance=Decimal("50000"),
                payment_method="کارت‌خوان",
                description="دریافتی بابت تسویه فاکتور"
            ),

            FinancialTransaction(
                transaction_number="TXN-100004",
                customer_id=customers[1].id,
                transaction_type="Opening balance",
                credit_amount=Decimal("200000"),
                running_balance=Decimal("-200000"),
                description="مانده ابتدای دوره"
            ),
            FinancialTransaction(
                transaction_number="TXN-100005",
                customer_id=customers[1].id,
                transaction_type="Sales invoice",
                debit_amount=Decimal("90000"),
                running_balance=Decimal("-110000"),
                invoice_id=invoices[1].id,
                description="فاکتور شماره INV-2026-0002"
            )
        ]

        for tx in transactions:
            session.add(tx)
        session.flush()

        customers[0].current_balance = Decimal("50000")
        customers[1].current_balance = Decimal("-110000")
