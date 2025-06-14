from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QWidget
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from threading import Thread
from time import sleep as wait
import asyncio

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

        self.mainlayout = QVBoxLayout(self)

        self.chatlist = QWidget()
        self.chatlist.chats = []
        self.chatlistlayout = QVBoxLayout(self.chatlist)

        self.chat = QWidget()
        
        self.chatlayout = QVBoxLayout(self.chat)

        self.mainlayout.addWidget(self.chatlist, stretch=3)
        self.mainlayout.addWidget(self.chat, stretch=7)
        tr = Thread(target=self.waitforready,args=())
        tr.start()
        # Запуск Telethon в отдельном потоке
        self.thread = AsyncThread(self.tg_client)
        self.thread.message_received.connect(self.update_chat)
        self.thread.start()

    def waitforready(self):
        while not(self.tg_client.loaded):
            wait(0.1)
        self.loadchats()
    def send_message(self):
        pass

    def update_chat(self, message):
        pass
    
    def openchat(self,dialog):
        if id == -1:
            QMessageBox.warning(text="Этот чат загрузился не правильно!\nПопробуйте перезапустить приложение.", title="Что-то пошло не так.")
            return
    
    def create_chat_btn(self,name:str = "bad chat",id:int = -1):
        btn = QPushButton(self.chatlist)
        btn.text=name
        btn.clicked.connect(lambda: self.openchat(id))


    def loadchats(self):
        chats = self.getchats()
        self.chatlist.chats = []
        for chat in chats:
            o = self.create_chat_btn(chat.name,chat.id)
            self.chatlist.chats.append(o)
            self.chatlistlayout.addWidget(o)
            

    async def getchats(self):
        return await self.tg_client.get_dialogs()