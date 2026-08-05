@echo off
echo Building Lab & Ledger Windows Desktop Executable...
pip install -r requirements.txt
pyinstaller --noconfirm --windowed --name "LabCustomerLedger" main.py
echo Build Completed successfully!
pause
