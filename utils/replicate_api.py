"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
import os

import replicate
from httpcore import ReadTimeout

from bot_start import logger
from src.config import Configuration
from utils.create_google_doc import create_doc_func
from utils.make_gs import get_prompt_gs
from utils.openai_api import openai_func

os.environ["REPLICATE_API_TOKEN"] = Configuration.replicate_token


async def replicate_api_func(call_list, access_token):
    logger.info(f'Start replicate api')
    new_call_list = []
    prompt = await get_prompt_gs()
    for record in call_list:
        replicate_url = record.get('content') + f'?access_token={access_token}'
        logger.info(f'Make replicate url --> {replicate_url} ')
        try:
            while True:
                output = await replicate.async_run(
                    Configuration.replicate_model,
                    input={
                        "file": replicate_url,
                        "prompt": '',
                        "group_segments": True,
                        "offset_seconds": 0,
                        "transcript_output_format": "segments_only"
                    },
                    timeout=300
                )
                if output is None:
                    continue
                else:
                    break
        except ReadTimeout:
            logger.warning('Replicate timeout')
            raise
        except Exception as _ex:
            logger.warning(f'Skip Replicate Error: {_ex}')
            continue
        logger.info(f'Relicate Output --> {output}')
        if not output:
            logger.error(f'Replicate None')
            continue

        def format_time(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = seconds % 60
            return f"{hours:02}:{minutes:02}:{seconds:05.2f}".replace('.', ':')

        text_str = ''
        for segment in output['segments']:
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            speaker = segment['speaker']
            text = segment['text']
            text_str += f"[{start_time} - {end_time} - {speaker}]\n"
            text_str += f'{text}\n'

        doc_url = await create_doc_func(text_str)
        mistake, conversation_assessment, jtbd, overall_assessment = await openai_func(text_str, prompt)
        new_call_list.append({
            'direction': record.get('direction'),
            'id': record.get('id'),
            'from': record.get('from'),
            'to': record.get('to'),
            'content': record.get('content'),
            'duration': record.get('duration'),
            'start_time': record.get('start_time'),
            'doc_url': doc_url,
            'mistake': mistake,
            'conversation_assessment': conversation_assessment,
            'jtbd': jtbd,
            'overall_assessment': overall_assessment})
    logger.info(f'End replicate api')
    return new_call_list
