"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
from datetime import datetime, timedelta

from bot_start import scheduler, bot, logger
from src.config import Configuration
from utils.get_records import get_speak_func
from utils.make_gs import gspread_func
from utils.replicate_api import replicate_api_func


async def main_func():
    logger.info('Start scheduler')
    call_list, access_token, count_calls = await get_speak_func()
    if not call_list:
        for admin_id in Configuration.admin_ids:
            await bot.send_message(
                chat_id=admin_id,
                text=f'📌 <b>Нет данных для обновления</b>',
                disable_web_page_preview=True
            )
            return
    new_call_list = await replicate_api_func(call_list, access_token)
    gs_url = await gspread_func(new_call_list)
    for admin_id in Configuration.admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=f'<b>📌 Обновил данные в вашей таблице: \n\n'
                 f'📋 Новых записей -- {count_calls}\n\n'
                 f'🔗 Ссылка на таблицу</b>\n'
                 f'{gs_url}',
            disable_web_page_preview=True)
    logger.info('End scheduler')


async def create_scheduler():
    scheduler.add_job(main_func, 'interval', minutes=30, next_run_time=datetime.now() + timedelta(seconds=1))
