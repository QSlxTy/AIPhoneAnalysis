"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.bot.dispatcher import get_dispatcher
from src.config import conf

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = AsyncIOScheduler(jobstores=jobstores)
bot = Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode='HTML'))
storage = MemoryStorage()
logger = logging.getLogger(__name__)
dp = get_dispatcher(storage=storage)
