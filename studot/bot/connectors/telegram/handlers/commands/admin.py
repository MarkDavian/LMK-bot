from aiogram import types, Dispatcher
from aiogram.types import ContentTypes
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from config import settings

from bot.core.data_parser.JSONParser.parser import JSONParser
from bot.core.data_parser.PDFParser.csv_parser import CSVParser
from bot.core.notifier.notifier import notifier
from bot.core.file_resolver.resolver import File
from bot.core.statistics.proxy.proxy_users_db import usersDB
from bot.core.utils.types.userinfo import UserInfo


async def get_user_info(user_id: int) -> UserInfo:
    userInfo = await usersDB.get_user_info(user_id)

    return userInfo


class UpdateChangesSG(StatesGroup):
    start = State()
    csv_set = State()

    notify_preset = State()
    notify_set = State()

    shedule_from_xlsx = State()
    shedule_from_json = State()


async def cmd_update_changes(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id not in settings.admins_id:
        return

    await message.answer(
        'Напиши дату замен в формате ГГГГ-ММ-ДД'
    )

    await state.set_state(UpdateChangesSG.start.state)
    

async def get_date(message: types.Message, state: FSMContext):
    date = message.text

    await message.answer(
        'Теперь пришли таблицу CSV с заменами'
    )

    await state.set_state(UpdateChangesSG.csv_set.state)
    await state.update_data(date=date)


async def get_file_csv(message: types.Message, state: FSMContext):
    await message.answer(
        'Получил файл, обрабатываю'
    )
    file_info = await message.bot.get_file(message.document.file_id)
    filepath = File('new_changes.csv')
    file = await message.bot.download_file(file_info.file_path, destination=filepath)

    await process_file(filepath, message, state)


async def process_file(filepath, message: types.Message, state: FSMContext):
    data = await state.get_data()
    date = data['date']
    await state.finish()

    csvParser = CSVParser(csv_filepath=filepath)
    csvParser.process()
    dict_to_parse = csvParser.dict()
    jsonParser = JSONParser(dict_to_parse=dict_to_parse)
    changes = jsonParser.parse()
    new_changes_path = File('new_changes.json')
    with open(new_changes_path, 'w') as file:
        import json
        json.dump(changes, file, ensure_ascii=False, indent=4, sort_keys=True)

    with open(new_changes_path, 'rb') as file:
        await message.bot.send_message(settings.admin_id, 'Обработал')
        await message.bot.send_document(settings.admin_id, file)

    await save_to_db(changes, date)
    await notifier.notify_changes()


async def save_to_db(changes: dict, date: str):
    from bot.core.utils.db.shedule import sheduleDB
    await sheduleDB.save_change_shedule(changes, date)






async def cmd_get_metrcis_csv(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id not in settings.admins_id:
        return
    
    with open('data/metrics/metrics.csv', 'rb') as file:
        await message.bot.send_document(message.from_user.id, file)






async def cmd_notify_all(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id not in settings.admins_id:
        return
    
    await state.set_state(UpdateChangesSG.notify_preset.state)

    await message.answer(
        'Напиши сообщение для пользователей:'
    )
    

async def pre_notify_all(message: types.Message, state: FSMContext):
    text = message.text

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Отправить')
    keyboard.add('Отменить')

    await state.update_data(text=text)
    await state.set_state(UpdateChangesSG.notify_set.state)

    await message.answer(
        'Вот твой текст, проверь его:\n'+text,
        reply_markup=keyboard
    )


async def notify_all(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data['text']

    if message.text.lower() == 'отправить':
        await notifier.notify_users(text)
        await message.answer('Текст отправлен пользователям')
    elif message.text.lower() == 'отменить':
        await message.answer('Отменено. Текст не отправлен')
    else:
        await message.answer('Используй кнопки')
        return
    
    await state.finish()






async def cmd_get_shedule_json_from_xlsx(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id not in settings.admins_id:
        return
    
    await state.set_state(UpdateChangesSG.shedule_from_xlsx.state)

    await message.answer(
        'Отправь файл расписания XLSX'
    )

async def pre_get_shedule(message: types.Message, state: FSMContext):
    await message.answer(
        'Получил файл, обрабатываю'
    )
    file_info = await message.bot.get_file(message.document.file_id)
    filepath = File('curs.xlsx')
    file = await message.bot.download_file(file_info.file_path, destination=filepath)

    await get_shedule(filepath, message)
    await state.finish()


async def get_shedule(filepath, message: types.Message):
    from bot.connectors.telegram.handlers.commands.mainSheduleParser import MainSheduleParser

    parser = MainSheduleParser(filepath)
    final, tmp = await parser.parse()

    with open(final, 'rb') as final_io, open(tmp, 'rb') as tmp_io:
        await message.bot.send_document(
            message.from_user.id, 
            tmp_io, 
            caption='Технический файл. Нужен только для отладки'
        )
        await message.bot.send_document(
            message.from_user.id, 
            final_io, 
            caption='Результат парса расписания'
        )






async def cmd_get_parsed(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id not in settings.admins_id:
        return
    
    await state.set_state(UpdateChangesSG.shedule_from_xlsx.state)

    await message.answer(
        'Отправь файл расписания JSON'
    )


async def pre_get_parsed(message: types.Message, state: FSMContext):
    await message.answer(
        'Получил файл, обрабатываю'
    )
    file_info = await message.bot.get_file(message.document.file_id)
    filepath = File('curs_shedule.json')
    file = await message.bot.download_file(file_info.file_path, destination=filepath)

    await get_parsed(filepath, message)
    await state.finish()


async def get_parsed(filepath, message: types.Message):
    from bot.connectors.telegram.handlers.commands.sheduleParser import SheduleParser

    parser = SheduleParser(filepath)
    final = await parser.parse()

    with open(final, 'rb') as final_io:
        await message.bot.send_document(
            message.from_user.id, 
            final_io, 
            caption='Результат парса расписания'
        )


def register_admin_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_update_changes, commands="set_changes", state="*")
    dp.register_message_handler(cmd_get_metrcis_csv, commands="metrics", state="*")
    dp.register_message_handler(get_date, state=UpdateChangesSG.start)
    dp.register_message_handler(get_file_csv, state=UpdateChangesSG.csv_set, content_types=ContentTypes.DOCUMENT)

    dp.register_message_handler(cmd_notify_all, commands="notify", state="*")
    dp.register_message_handler(pre_notify_all, state=UpdateChangesSG.notify_preset)
    dp.register_message_handler(notify_all, state=UpdateChangesSG.notify_set)

    dp.register_message_handler(cmd_get_shedule_json_from_xlsx, commands="get_json", state="*")
    dp.register_message_handler(pre_get_shedule, state=UpdateChangesSG.shedule_from_xlsx, content_types=ContentTypes.DOCUMENT)

    dp.register_message_handler(cmd_get_parsed, commands="parse_json", state="*")
    dp.register_message_handler(pre_get_parsed, state=UpdateChangesSG.shedule_from_json, content_types=ContentTypes.DOCUMENT)
