import sys
from PyQt6.QtWidgets import QApplication

from telethon.sessions import StringSession
from PyQt6.QtCore import QObject, pyqtSignal,Qt
import asyncio
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QWidget, QScrollArea, QHBoxLayout
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from threading import Thread
from time import sleep as wait
from telethon.network import ConnectionTcpMTProxyRandomizedIntermediate
from telethon import TelegramClient, events

API_ID = 21390934
API_HASH = "12f62a29ab589e36b4a8a5a1e135dfda"

window = None
tg_manager = None
class TelegramManager:  # Переименуем класс, чтобы избежать путаницы
    def __init__(self, api_id, api_hash, phone):
        self.loaded = False
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        # Используем telethon.TelegramClient, а не наш класс!
        self.client = TelegramClient(StringSession(), api_id, api_hash)
        self.setup_handlers()


    async def start(self):
        await self.client.start(self.phone)
        print("Успешная авторизация!")
        window.loadchats()
        dialogs = await self.client.get_dialogs()
        
        

    def setup_handlers(self):
        @self.client.on(events.NewMessage)
        async def handler(event):
            print(f"Новое сообщение: {event.text}")

    async def send_message(self, receiver, text):
        await self.client.send_message(receiver, text)



class AsyncThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        asyncio.run(self.client.start())

class MainWindow(QMainWindow):
    def __init__(self, tg_client):
        super().__init__()
        self.tg_client = tg_client
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Turbo Telegram")
        self.setGeometry(300, 300, 600, 400)

        # Главный контейнер
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout (горизонтальный)
        main_layout = QHBoxLayout(central_widget)

        # ===== Чат-лист с прокруткой =====
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Важно!

        # Контейнер для кнопок чатов
        self.chatlist_container = QWidget()
        self.chatlist_layout = QVBoxLayout(self.chatlist_container)
        self.chatlist_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Выравнивание сверху

        scroll_area.setWidget(self.chatlist_container)
        # =================================

        # Правая часть (чат)
        self.chat_widget = QTextEdit()
        self.chat_widget.setReadOnly(True)

        # Распределение пространства
        main_layout.addWidget(scroll_area, stretch=2)  # 2/5 ширины
        main_layout.addWidget(self.chat_widget, stretch=3)  # 3/5 ширины

        # Настройки скролла
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    def send_message(self):
        pass

    def update_chat(self, message):
        pass
    
    def openchat(self,dialog):
        if id == -1:
            QMessageBox.warning(text="Этот чат загрузился не правильно!\nПопробуйте перезапустить приложение.", title="Что-то пошло не так.")
            return
    

    async def load_chats(self):
        # Очищаем предыдущие чаты
        self.clear_chat_list()
        
        try:
            # Получаем диалоги асинхронно
            dialogs = await self.tg_client.client.get_dialogs()
            
            # Сортируем: сначала закрепленные, потом по дате
            dialogs.sort(key=lambda d: (not d.pinned, d.date), reverse=True)
            
            for dialog in dialogs:
                self.add_chat_to_list(
                    name=dialog.name,
                    chat_id=dialog.id,
                    unread=dialog.unread_count,
                    is_pinned=dialog.pinned
                )
                
        except Exception as e:
            self.show_error(f"Ошибка загрузки: {str(e)}")

    def clear_chat_list(self):
        # Очищаем layout
        for i in reversed(range(self.chatlist_layout.count())): 
            widget = self.chatlist_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def add_chat_to_list(self, name, chat_id, unread=0, is_pinned=False):
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setFixedHeight(60)
        
        # Стилизация кнопки
        style = f"""
        QPushButton {{
            text-align: left;
            padding: 8px;
            border: none;
            border-bottom: 1px solid #eee;
            font-size: 14px;
            { "background-color: #f5f5f5;" if is_pinned else "" }
        }}
        QPushButton:hover {{ background-color: #e9e9e9; }}
        """
        
        # Иконка непрочитанных
        unread_badge = ""
        if unread > 0:
            unread_badge = f"""<span style="
                background: #0088cc;
                color: white;
                border-radius: 10px;
                padding: 2px 6px;
                font-size: 12px;
                margin-left: 10px;
            ">{unread}</span>"""
        
        btn.setText(f"""
        <div style="font-weight: bold;">{name}</div>
        <div style="color: #888; font-size: 12px;">ID: {chat_id}{unread_badge}</div>
        """)
        btn.setStyleSheet(style)
        btn.clicked.connect(lambda: self.open_chat(chat_id))
        
        self.chatlist_layout.addWidget(btn)

    def create_chat_btn(self,name:str = "bad chat",id:int = -1):
        btn = QPushButton(self.chatlist)
        btn.text=name
        btn.clicked.connect(lambda: self.openchat(id))
    
    def add_chat_button(self, chat_name, chat_id):
        btn = QPushButton(chat_name)
        btn.setFixedHeight(40)  # Фиксированная высота кнопки
        btn.setStyleSheet("""
        QPushButton {
            text-align: left;
            padding: 5px;
            border: none;
            border-bottom: 1px solid #eee;
        }
        QPushButton:hover {
            background-color: #f5f5f5;
        }
    """)
        self.chatlist_layout.addWidget(btn)


    async def loadchats(self):
        chats = await self.getchats()
        self.chatlist.chats = []

        for i in reversed(range(self.chatlistlayout.count())): 
            self.chatlistlayout.itemAt(i).widget().deleteLater()
    
        # Добавляем новые
        for chat in chats:
            btn = self.create_chat_btn(chat.name, chat.id)
            self.chatlistlayout.addWidget(btn)


        for chat in chats:
            o = self.create_chat_btn(chat.name,chat.id)
            self.chatlist.chats.append(o)
            self.chatlistlayout.addWidget(o)
            

    async def getchats(self):
        return await self.tg_client.get_dialogs()


PHONE = input("Your phone: ")
def main():
    global tg_manager
    global window
    global PHONE
    #app = QApplication(sys.argv)
    
    tg_manager = TelegramManager(API_ID, API_HASH, PHONE)  # Используем TelegramManager
    #window = MainWindow(tg_manager)
    #window.show()
    
    

    #sys.exit(app.exec())

if __name__ == "__main__":
    main()

