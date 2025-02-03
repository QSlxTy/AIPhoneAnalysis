"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
from dotenv import load_dotenv
from ringcentral import SDK

from bot_start import logger
from src.config import Configuration

load_dotenv()


async def generate_code_func():
    logger.info('Start Generate Access Token')
    rcsdk = SDK(Configuration.client_id, Configuration.client_secret, Configuration.server_url)
    platform = rcsdk.platform()
    try:
        platform.login(jwt=Configuration.jwt)
        access_token = platform.auth().data().get('access_token')
        logger.info(f'Success Generate Access Token: {access_token}')
        return access_token
    except Exception as e:
        logger.error(f'Generate Access Token Error: {e}')
