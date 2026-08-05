import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOC_DIR = os.path.join(BASE_DIR, 'documents')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOC_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Database Configuration
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'lab_manager.db')}"

# Application Settings Default
APP_TITLE = "سامانه مدیریت گزارش‌های آزمایشگاهی و حساب مشتریان"
DEFAULT_THEME = "dark"  # light / dark
DEFAULT_CURRENCY = "Toman"  # Rial / Toman
BALANCE_CONVENTION = "DEBIT_INCREASES_OWED"  # Positive means customer is debtor (بدهکار)

# OCR falling options
DEFAULT_OCR_LANG = "fas+eng"
DEFAULT_DPI = 300
DEFAULT_ZOOM = 1.0

# Fonts
FONT_NAME = "Vazirmatn"
