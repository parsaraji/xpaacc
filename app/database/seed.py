import datetime
from decimal import Decimal
from app.database.session import get_db_session
from app.models.customer import Customer
from app.models.transaction import FinancialTransaction
from app.models.invoice import Invoice, InvoiceItem
from app.models.laboratory_report import LaboratoryReport
from app.models.laboratory_test import LaboratoryTestResult
from app.models.extraction_template import ExtractionTemplate

def seed_initial_data():
    with get_db_session() as session:
        if session.query(Customer).count() > 0:
            return

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
            ),
            Customer(
                customer_code="CUS-000003",
                customer_type="دامپزشک",
                first_name="دکتر امین",
                last_name="سهرابی",
                display_name="دکتر امین سهرابی",
                mobile="09123333333",
                province="اصفهان",
                city="اصفهان"
            ),
            Customer(
                customer_code="CUS-000004",
                customer_type="کلینیک",
                company_name="کلینیک دامپزشکی مهر",
                display_name="کلینیک دامپزشکی مهر",
                mobile="09124444444",
                province="فارس",
                city="شیراز"
            ),
            Customer(
                customer_code="CUS-000005",
                customer_type="آزمایشگاه",
                company_name="آزمایشگاه همکار پایتخت",
                display_name="آزمایشگاه همکار پایتخت",
                mobile="09125555555",
                province="خراسان رضوی",
                city="مشهد"
            )
        ]

        for cust in customers:
            session.add(cust)
        session.flush()

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
            ),
            LaboratoryReport(
                report_number="REP-9003",
                customer_id=customers[2].id,
                patient_name="بیمار شماره ۳",
                sample_id="SMP-300",
                sample_type="Blood",
                test_date="9/11/2026 09:00:00 AM",
                send_date="9/11/2026 09:05:00 AM",
                print_date="9/11/2026 10:15:00 PM",
                original_filename="report_3.xps",
                review_status="نیازمند بررسی"
            )
        ]

        for rep in reports:
            session.add(rep)
        session.flush()

        test_results = [
            LaboratoryTestResult(report_id=reports[0].id, test_name="SGPT", value_text="16.1", unit="U/L", result_status="Normal", row_number=1),
            LaboratoryTestResult(report_id=reports[0].id, test_name="SGOT", value_text="13.2", unit="U/L", result_status="Normal", row_number=2),
            LaboratoryTestResult(report_id=reports[0].id, test_name="ALP", value_text="0", unit="U/L", result_status="Normal", row_number=3),

            LaboratoryTestResult(report_id=reports[1].id, test_name="Hemoglobin", value_text="14.5", unit="g/dL", result_status="Normal", row_number=1),
            LaboratoryTestResult(report_id=reports[1].id, test_name="WBC", value_text="7.2", unit="10^3/uL", result_status="Normal", row_number=2),

            LaboratoryTestResult(report_id=reports[2].id, test_name="Urea", value_text="85", unit="mg/dL", result_status="High", row_number=1)
        ]

        for tr in test_results:
            session.add(tr)
        session.flush()

        invoices = [
            Invoice(
                invoice_number="INV-2026-0001",
                customer_id=customers[0].id,
                report_id=reports[0].id,
                total_amount=Decimal("150000"),
                paid_amount=Decimal("100000"),
                payment_status="بخشی تسویه‌شده"
            ),
            Invoice(
                invoice_number="INV-2026-0002",
                customer_id=customers[1].id,
                report_id=reports[1].id,
                total_amount=Decimal("250000"),
                paid_amount=Decimal("250000"),
                payment_status="تسویه‌شده"
            ),
            Invoice(
                invoice_number="INV-2026-0003",
                customer_id=customers[2].id,
                report_id=reports[2].id,
                total_amount=Decimal("300000"),
                paid_amount=Decimal("0"),
                payment_status="تسویه‌شده"
            )
        ]

        for inv in invoices:
            session.add(inv)
        session.flush()

        invoice_items = [
            InvoiceItem(invoice_id=invoices[0].id, item_name="هزینه آزمایش SGPT/SGOT", quantity=1, unit_price=Decimal("150000"), total_price=Decimal("150000")),
            InvoiceItem(invoice_id=invoices[1].id, item_name="هزینه نمونه‌گیری خون", quantity=1, unit_price=Decimal("250000"), total_price=Decimal("250000")),
            InvoiceItem(invoice_id=invoices[2].id, item_name="خدمات تخصصی آزمایشگاهی", quantity=1, unit_price=Decimal("300000"), total_price=Decimal("300000")),
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
                debit_amount=Decimal("150000"),
                running_balance=Decimal("200000"),
                invoice_id=invoices[0].id,
                description="فاکتور آزمایش شماره INV-2026-0001"
            ),
            FinancialTransaction(
                transaction_number="TXN-100003",
                customer_id=customers[0].id,
                transaction_type="Customer payment received",
                credit_amount=Decimal("100000"),
                running_balance=Decimal("100000"),
                payment_method="کارت‌خوان",
                description="دریافتی از مشتری"
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
                debit_amount=Decimal("250000"),
                running_balance=Decimal("50000"),
                invoice_id=invoices[1].id,
                description="فاکتور شماره INV-2026-0002"
            ),
            FinancialTransaction(
                transaction_number="TXN-100006",
                customer_id=customers[1].id,
                transaction_type="Customer payment received",
                credit_amount=Decimal("250000"),
                running_balance=Decimal("-200000"),
                payment_method="کارت به کارت",
                description="تسویه فاکتور INV-2026-0002"
            ),

            FinancialTransaction(
                transaction_number="TXN-100007",
                customer_id=customers[2].id,
                transaction_type="Sales invoice",
                debit_amount=Decimal("300000"),
                running_balance=Decimal("300000"),
                invoice_id=invoices[2].id,
                description="فاکتور ثبت شده INV-2026-0003"
            ),
            FinancialTransaction(
                transaction_number="TXN-100008",
                customer_id=customers[2].id,
                transaction_type="Customer payment received",
                credit_amount=Decimal("100000"),
                running_balance=Decimal("200000"),
                payment_method="نقدی",
                description="پیش‌پرداخت"
            ),
            FinancialTransaction(
                transaction_number="TXN-100009",
                customer_id=customers[3].id,
                transaction_type="Debit transaction",
                debit_amount=Decimal("120000"),
                running_balance=Decimal("120000"),
                description="تراکنش بدهی دستی"
            ),
            FinancialTransaction(
                transaction_number="TXN-100010",
                customer_id=customers[4].id,
                transaction_type="Credit transaction",
                credit_amount=Decimal("80000"),
                running_balance=Decimal("-80000"),
                description="تراکنش بستانکاری دستی"
            )
        ]

        for tx in transactions:
            session.add(tx)
        session.flush()

        customers[0].current_balance = Decimal("100000")
        customers[1].current_balance = Decimal("-200000")
        customers[2].current_balance = Decimal("200000")
        customers[3].current_balance = Decimal("120000")
        customers[4].current_balance = Decimal("-80000")
