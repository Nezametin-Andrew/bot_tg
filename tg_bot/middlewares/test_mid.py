import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


# class TestMidlWare(BaseMiddleware):
#
#     def __init__(self):
#         super().__init__()
#
#     async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
#         await cq.answer()