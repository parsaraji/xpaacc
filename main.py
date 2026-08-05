import sys
import os
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.database.connection import init_db
from app.database.seed import seed_initial_data

def main():
    # Initialize the local database directory and schema
    init_db()
    seed_initial_data()

    app = QApplication(sys.argv)
    app.setLayoutDirection(app.layoutDirection().RightToLeft)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
