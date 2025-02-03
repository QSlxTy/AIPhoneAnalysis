"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
import requests

from bot_start import logger
from src.config import Configuration
from utils.generate_code import generate_code_func
from utils.make_gs import get_ids


async def get_speak_func():
    logger.info("Start get records")
    url = (f'https://platform.ringcentral.com/restapi/v1.0/account/'
           f'{Configuration.account_id}/extension/{Configuration.extension_id}/call-log')
    access_token = await generate_code_func()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    logger.info(headers)
    call_list = []
    used_ids = await get_ids()
    count_calls = 0
    if response.status_code == 200:
        call_log = response.json()
        for record in call_log.get('records', []):
            logger.info('Record --> ' + str(record))
            logger.info('Get record, duration --> ' + str(record.get('duration')) + ' --> ' + str(record.get('id')))
            if record.get('id') in used_ids:
                logger.info('ID is exists -- > ' + str(record.get('id')))
                continue
            if record.get("result") in ['No Answer', 'Missed', 'Call Failed', 'Hang Up', 'IP Phone Offline']:
                logger.info('No result -- > ' + str(record.get('id')))
                continue
            try:
                record.get('recording').get('contentUri')
            except Exception as _ex:
                continue
            if record.get('from', {}).get('name'):
                from_info = record.get('from', {}).get('phoneNumber') + ',' + record.get('from', {}).get('name')
            else:
                from_info = record.get('from', {}).get('phoneNumber')
            if record.get('to', {}).get('name'):
                to_info = record.get('to', {}).get('phoneNumber') + ',' + record.get('to', {}).get('name')
            else:
                to_info = record.get('to', {}).get('phoneNumber')
            call_list.append({
                'direction': record.get('direction'),
                'id': record.get('id'),
                'from': from_info,
                'to': to_info,
                'content': record.get('recording').get('contentUri'),
                'duration': record.get('duration'),
                'start_time': record.get('startTime')})
            count_calls += 1
        logger.info(f"Success get records")

        return call_list, access_token, count_calls
    else:
        logger.error(f"Error get records: {response.status_code}")
        logger.error(response.json())
        return None
