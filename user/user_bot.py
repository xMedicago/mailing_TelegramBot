from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

# hash и id можно взять на сайте https://my.telegram.org/
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# user
client = TelegramClient("SESSION_NAME", api_id, api_hash).start()
