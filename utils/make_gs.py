"""
https://github.com/QSlxTy
Трифонов К.Е (QSlxTy)
"""
import gspread
from gspread_formatting import get_effective_format, Color, TextFormat, format_cell_range, CellFormat, set_column_width
from oauth2client.service_account import ServiceAccountCredentials

from bot_start import logger
from src.config import Configuration


async def gspread_func(new_call_list):
    logger.info(f'Start make gs')
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        Configuration.goohle_path,
        scope)
    client = gspread.authorize(credentials)

    try:
        sheet = client.open("Calls")
    except Exception as _ex:
        sheet = client.create("Calls")
        sheet.del_worksheet(sheet.worksheet('Sheet1'))
    try:
        worksheet = sheet.worksheet('Calls')
    except Exception as _ex:
        worksheet = sheet.add_worksheet(title='Calls', rows=1000, cols=20)
    if not worksheet.row_values(1):
        headers = [
            "direction", "Кому", "От", "ID", "Запись", "Длительность", "Время начала", "Расшифровка", 'Ошибки',
            'Оценка разговора', 'Боли, потребности JTBD клиента', 'Общая оценка'
        ]
        worksheet.append_row(headers)
    effective_format = get_effective_format(worksheet, 'A1')
    if 'red=0.84705883;green=0.8117647;blue=0.69803923' == str(effective_format.backgroundColor):
        logger.info(f"Redacted")
    else:
        logger.info("Start redaction")
        column_range = 'A1:N1'
        format_cell_range(worksheet, column_range, CellFormat(
            backgroundColor=Color(40, 49, 78),
            textFormat=TextFormat(bold=True),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
        ))
        column_range = 'L1:L1'
        format_cell_range(worksheet, column_range, CellFormat(
            backgroundColor=Color(84, 57, 100),
            textFormat=TextFormat(bold=True),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
        ))
        cell_range = 'A2:N500'
        format_cell_range(worksheet, cell_range, CellFormat(
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
            wrapStrategy='WRAP'
        ))
        worksheet.format('A1:M1', {'wrapStrategy': 'WRAP'})
        set_column_width(worksheet, 'A', 135)
        set_column_width(worksheet, 'B', 135)
        set_column_width(worksheet, 'C', 135)
        set_column_width(worksheet, 'D', 135)
        set_column_width(worksheet, 'E', 135)
        set_column_width(worksheet, 'F', 135)
        set_column_width(worksheet, 'G', 135)
        set_column_width(worksheet, 'H', 135)
        set_column_width(worksheet, 'I', 500)
        set_column_width(worksheet, 'J', 600)
        set_column_width(worksheet, 'K', 400)
        set_column_width(worksheet, 'L', 250)

    for record in new_call_list:
        logger.info('Gspread record --> ' + str(record))
        conversation_assessment = record.get('conversation_assessment').get('response')
        conversation_assessment_str = ''
        for conversation in conversation_assessment:
            conversation_assessment_str += conversation.get('criterion') + ': ' + conversation.get('analysis') + '\n'
        mistake_str = record.get('mistake').get('response')
        jtbds = record.get('jtbd').get('response')
        first = 'Боли: ' + str(jtbds.get('боли')).replace('[', '').replace(']', '') + '\n'
        second = 'Потребности: ' + str(jtbds.get('потребности')).replace('[', '').replace(']', '') + '\n'
        threed = 'JTBD: ' + str(jtbds.get('JTBD')).replace('[', '').replace(']', '') + '\n'
        jtbd_str = first + second + threed
        new_data = [
            record.get('direction'),  # A
            record.get('to'),  # B
            record.get('from'),  # C
            record.get('id'),  # D
            record.get('content'),  # E
            record.get('duration'),  # F
            record.get('start_time'),  # G
            record.get('doc_url'),  # H
            mistake_str,  # I
            conversation_assessment_str,  # J
            jtbd_str,  # K
            str(record.get('overall_assessment').get('response'))  # L
        ]

        worksheet.append_row(new_data)
    sheet.share('', perm_type='anyone', role='writer')
    link = sheet.url

    logger.info(f'End make gs')
    return link


async def get_ids():
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        Configuration.goohle_path,
        scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Calls")
    worksheet = sheet.worksheet('Calls')
    column_b_values = worksheet.col_values(4)
    return column_b_values


async def get_prompt_gs():
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        Configuration.goohle_path,
        scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Calls")
    worksheet = sheet.worksheet('Prompt')
    cell_value = worksheet.cell(1, 1).value
    return str(cell_value)
