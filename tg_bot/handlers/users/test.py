# from aiogram import types
#
# from bot_tg.loader import dp

import redis

r = redis.Redis(host='localhost', port=6379, db=0, encoding='utf-8')
r.set('foo', 'bar')
print(r.get('foo').decode())
