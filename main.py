import sys
from PyQt6.QtWidgets import QApplication
from ui.mainwindow import MainWindow
from telegram_client import TelegramManager

# Конфиг (вынесите в config.py)
API_ID = 21390934
API_HASH = "12f62a29ab589e36b4a8a5a1e135dfda"
PHONE = input("Your phone: ")




def main():
    
    app = QApplication(sys.argv)
    
    tg_manager = TelegramManager(API_ID, API_HASH, PHONE)  # Используем TelegramManager
    window = MainWindow(tg_manager)
    window.show()
    
    

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

