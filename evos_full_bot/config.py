import os
from dotenv import load_dotenv

load_dotenv()  # .env faylini yuklaydi

token = os.getenv("TOKEN")
DB_PATH = os.getenv("DB_PATH", "fast_food.db")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
LANGUAGES = ['uz', 'ru', 'en']
