"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
from datetime import datetime

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from bot_start import logger
from src.config import Configuration


async def create_doc_func(text):
    logger.info(f'Start create google doc')
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive",
             'https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        Configuration.goohle_path,
        scope)
    service = build('docs', 'v1', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)

    document = {
        'title': str(datetime.now()),
    }
    doc = service.documents().create(body=document).execute()
    document_id = doc.get('documentId')
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        }
    ]
    service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    permission_body = {
        'role': 'reader',
        'type': 'anyone'
    }

    drive_service.permissions().create(
        fileId=document_id,
        body=permission_body,
        fields='id'
    ).execute()
    document_link = f"https://docs.google.com/document/d/{document_id}/edit"
    logger.info(f'End create google doc --> {document_link}')
    return document_link
