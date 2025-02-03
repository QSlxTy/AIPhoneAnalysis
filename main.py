"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
import asyncio
import logging

from bot_start import dp, bot, scheduler
from src.config import conf
from utils.scheduler import create_scheduler


async def start_bot():
    await create_scheduler()
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=conf.logging_level)
        logging.getLogger('matplotlib.font_manager').disabled = True
        logging.getLogger('httpcore.http11').disabled = True
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
    finally:
        scheduler.remove_all_jobs()
