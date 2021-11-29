from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
#from .test_mid import TestMidlWare


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
   # dp.middleware.setup(TestMidlWare())
