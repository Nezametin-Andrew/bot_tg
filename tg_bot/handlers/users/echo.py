from aiogram import types
from tg_bot.loader import dp
import time
import urllib3
import json


http = urllib3.PoolManager()


@dp.message_handler(text="sdsd")
async def bot_echo(message: types.Message):
    start = time.time()
    r = http.request("GET", "http://localhost:8000/")
    print(time.time() - start)
    print(json.loads(r.data.decode()))
    await message.answer(message.text)
