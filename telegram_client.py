from telethon import TelegramClient, events
from telethon.sessions import StringSession
from PyQt6.QtCore import QObject, pyqtSignal
import asyncio

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
        self.loaded=True
        dialogs = await self.client.get_dialogs()
        
        

    def setup_handlers(self):
        @self.client.on(events.NewMessage)
        async def handler(event):
            print(f"Новое сообщение: {event.text}")

    async def send_message(self, receiver, text):
        await self.client.send_message(receiver, text)