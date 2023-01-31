import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.core.utils.types.userinfo import UserInfo
from bot.core.utils.types.shedule import SHEDULE_DAY
from bot.core.statistics.proxy.proxy_users_db import usersDB
from bot.core.statistics.proxy.proxy_shedule_db import sheduleDB


def get_userinfo(user_id: int) -> UserInfo:
    userInfo = usersDB.get_user_info(user_id)

    return userInfo


async def cmd_get_shedule_today(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    userInfo = get_userinfo(user_id)

    day = datetime.date.today().weekday()
    today = SHEDULE_DAY.WEEKDAYS[day]

    dayShedule = sheduleDB.get_day_shedule(today, userInfo)

    await message.answer(
        (
            f'Расписание на {dayShedule.name}:\n'+
            repr(dayShedule)
        )
    )


async def cmd_get_shedule_tomorrow(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    userInfo = get_userinfo(user_id)

    day = datetime.date.today().weekday()
    today = SHEDULE_DAY.WEEKDAYS[day+1]

    dayShedule = sheduleDB.get_day_shedule(today, userInfo)

    await message.answer(
        (
            f'Расписание на {dayShedule.name}:\n'+
            repr(dayShedule)
        )
    )


async def cmd_get_change_shedule(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    userInfo = get_userinfo(user_id)

    now_date = datetime.date.today()
    change_date = now_date+datetime.timedelta(days=1)
    dayShedule = sheduleDB.get_change_shedule(change_date, userInfo)

    text = 'Замен нет'
    if dayShedule is not None:
        if hasattr(dayShedule, 'name'):
            text = (f'Замены на {dayShedule.name}:\n'+
                    repr(dayShedule)
            )
        else:
            text = dayShedule

    await message.answer(
        text
    )


async def get_shedule_day(message: types.Message, state: FSMContext):
    day = ''
    user_id = message.from_user.id
    userInfo = get_userinfo(user_id)

    dayShedule = sheduleDB.get_day_shedule(day, userInfo)

    await message.answer(
        (
            f'Расписание на {day}:\n'+
            repr(dayShedule)
        )
    )


async def cmd_get_week_shedule(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    userInfo = get_userinfo(user_id)

    weekShedule = sheduleDB.get_week_shedule(userInfo)

    await message.answer(
        (
            f'Расписание на неделю:\n'+
            repr(weekShedule)
        )
    )



def register_shedule_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_get_shedule_today, commands="today", state="*")
    dp.register_message_handler(cmd_get_shedule_tomorrow, commands="tomorrow", state="*")
    dp.register_message_handler(cmd_get_change_shedule, commands="changes", state="*")
    dp.register_message_handler(cmd_get_week_shedule, commands="week", state="*")