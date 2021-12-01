import os
from pathlib import Path
from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"
BOT_TOKEN = dotenv_values(ENV_PATH)['TOKEN_TG']
admins = [
    1260426275
]

ip = dotenv_values(ENV_PATH)["IP"]

aiogram_redis = {
    'host': '188.72.209.127',
}

redis = {
    'address': ('188.72.209.127', 6379),
    'encoding': 'utf8'
}
