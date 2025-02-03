"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
import json

from openai import OpenAI

from bot_start import logger, bot
from src.config import Configuration

client = OpenAI(
    api_key=Configuration.openai_token)


async def openai_func(text, prompt):
    try:
        logger.info("Start openai api")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )
        logger.info("End openai api -> " + response.choices[0].message.content)
        json_output = json.loads(response.choices[0].message.content)
        mistake = json_output.get('mistake')
        conversation_assessment = json_output.get('conversation_assessment')
        jtbd = json_output.get('jtbd')
        overall_assessment = json_output.get('overall_assessment')
        return mistake, conversation_assessment, jtbd, overall_assessment
    except Exception as _ex:
        logger.error(f'OpenAI Error: {_ex}')
        for admin in Configuration.admin_ids:
            await bot.send_message(
                chat_id=admin,
                text=f'📌 <b>Ошибка в обработке OpenAI</b>{_ex}'
            )
        return
