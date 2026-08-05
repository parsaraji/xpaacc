import os
import shutil
import datetime
from sqlalchemy.orm import Session
from app.config import DATA_DIR, DOC_DIR, BACKUP_DIR
from app.database.connection import engine
import zipfile

class BackupService:
    def __init__(self, session: Session):
        self.session = session

    def create_backup(self) -> str:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.zip"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)

        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            db_file = os.path.join(DATA_DIR, 'lab_manager.db')
            if os.path.exists(db_file):
                zipf.write(db_file, arcname='lab_manager.db')

            for root, dirs, files in os.walk(DOC_DIR):
                for f in files:
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, os.path.dirname(DOC_DIR))
                    zipf.write(full_p, arcname=rel_p)

        return backup_path

    def restore_backup(self, zip_filepath: str):
        if not os.path.exists(zip_filepath):
            raise FileNotFoundError("فایل پشتیبان مشخص شده یافت نشد.")

        # Dispose of any active SQLAlchemy DB connection/locks on Windows
        engine.dispose()

        with zipfile.ZipFile(zip_filepath, 'r') as zipf:
            zipf.extractall(path=os.path.dirname(DATA_DIR))
