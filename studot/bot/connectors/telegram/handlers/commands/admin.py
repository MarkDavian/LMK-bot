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


def get_user_info(user_id: int) -> UserInfo:
    userInfo = usersDB.get_user_info(user_id)

    return userInfo


class UpdateChangesSG(StatesGroup):
    start = State()
    csv_set = State()


async def cmd_update_changes(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id != settings.admin_id:
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
    notifier.notify_changes()


async def save_to_db(changes: dict, date: str):
    from bot.core.utils.db.shedule import sheduleDB
    sheduleDB.save_change_shedule(changes, date)


def register_admin_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_update_changes, commands="update_changes", state="*")
    dp.register_message_handler(get_date, state=UpdateChangesSG.start)
    dp.register_message_handler(get_file_csv, state=UpdateChangesSG.csv_set, content_types=ContentTypes.DOCUMENT)
