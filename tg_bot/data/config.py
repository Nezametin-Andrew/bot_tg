import os
from pathlib import Path
from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = str(BASE_DIR) + "\.env"
BOT_TOKEN = dotenv_values(ENV_PATH)['TOKEN_TG']
admins = [
    1260426275
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
