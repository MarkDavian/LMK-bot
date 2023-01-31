import datetime

from vkbottle import BaseStateGroup, Keyboard, EMPTY_KEYBOARD, Text, KeyboardButtonColor
from vkbottle.bot import Message

from bot.connectors.vk.vk_bot_config import labeler, state_dispenser

from bot.core.utils.types.shedule import SHEDULE_DAY
from bot.core.statistics.proxy.proxy_shedule_db import sheduleDB

from bot.connectors.vk.menu.start_menu import MenuSG, get_user_info



@labeler.message(text='Расписание', state=MenuSG.start)
@labeler.message(text='Назад', state=MenuSG.additional)
async def menu_shedule_menu(message: Message):
    await state_dispenser.set(message.peer_id, MenuSG.start)

    keyboard = (
        Keyboard()
        .add(Text('Сегодня'))
        .add(Text('Замены'))
        .add(Text('Завтра'))
        .row()
        .add(Text('Эта неделя'))
        .add(Text('След. неделя'))
        .row()
        .add(Text('Дополнительно'))
        .row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )

    await message.answer(
        'Меню расписаний',
        keyboard=keyboard
    )

@labeler.message(text='Сегодня', state=MenuSG.start)
async def menu_get_today_shedule(message: Message):
    userInfo = get_user_info(message.from_id)

    day = datetime.date.today().weekday()
    today = SHEDULE_DAY.WEEKDAYS[day]

    dayShedule = sheduleDB.get_day_shedule(today, userInfo)

    await message.answer(
        (
            f'Расписание на {dayShedule.name}:\n'+
            repr(dayShedule)
        )
    )


@labeler.message(text='Завтра', state=MenuSG.start)
async def menu_get_tomorrow_shedule(message: Message):
    userInfo = get_user_info(message.from_id)

    day = datetime.date.today().weekday()
    today = SHEDULE_DAY.WEEKDAYS[day+1]

    dayShedule = sheduleDB.get_day_shedule(today, userInfo)

    await message.answer(
        (
            f'Расписание на {dayShedule.name}:\n'+
            repr(dayShedule)
        )
    )


@labeler.message(text='Замены', state=MenuSG.start)
async def menu_get_change_shedule(message: Message):
    userInfo = get_user_info(message.from_id)

    change_date = datetime.date.today() + datetime.timedelta(days=1)

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


@labeler.message(text='Эта неделя', state=MenuSG.start)
async def menu_get_this_week(message: Message):
    userInfo = get_user_info(message.from_id)

    shedule = sheduleDB.get_week_shedule(userInfo)

    await message.answer(
        repr(shedule)
    )


@labeler.message(text='След. неделя', state=MenuSG.start)
async def menu_get_next_week(message: Message):
    userInfo = get_user_info(message.from_id)

    shedule = sheduleDB.get_next_week_shedule(userInfo)
    
    await message.answer(
        repr(shedule)
    )


@labeler.message(text='Цвет недели', state=MenuSG.additional)
async def menu_week_color(message: Message):
    userInfo = get_user_info(message.from_id)

    color = sheduleDB.get_week_color(userInfo)

    await message.answer(color)


@labeler.message(text='Расписание на день', state=MenuSG.additional)
async def menu_day_shedule(message: Message):
    keyboard = (
        Keyboard()
        .add(Text('Понедельник')).row()
        .add(Text('Вторник')).row()
        .add(Text('Среда')).row()
        .add(Text('Четверг')).row()
        .add(Text('Пятница')).row()
        .add(Text('Суббота')).row()
        .add(Text('Назад'), KeyboardButtonColor.PRIMARY)
    )
    await message.answer(
        'Какой день?',
        keyboard=keyboard
    )
    await state_dispenser.set(message.peer_id, MenuSG.menuDayShedule)


@labeler.message(text='<day>', state=MenuSG.menuDayShedule)
async def day_shedule(message: Message, day=None):
    if day.lower() == 'назад':
        return await menu_shedule_menu(message)

    userInfo = get_user_info(message.from_id)

    shedule = sheduleDB.get_day_shedule(day, userInfo)

    await message.answer(
        (
            f'Расписание на {shedule.name}\n'+
            repr(shedule)
        )
    )

@labeler.message(text='Расписание звонков', state=MenuSG.additional)
async def rings_shedule(message: Message):
    userInfo = get_user_info(message.from_id)

    rings = sheduleDB.get_rings(userInfo)

    await message.answer(
        (
            f'Расписание звонков:\n'+
            rings
        )
    )