from vkbottle.bot import Message

from bot.core.utils.db.db import client

from bot.connectors.vk.vk_bot_config import labeler


telemetry = client['telemetry']


def save_message(message: Message) -> None:
    chat_id = message.chat_id
    user_id = message.from_id
    text = message.text
    # timestamp
    message_date = message.date

    name = 'chat_'+chat_id

    r = telemetry[name].insert_one(
            {
                'user_id': user_id,
                'text': text,
                'date': message_date
            }
    )


@labeler.chat_message()
async def collect_telemetry(message: Message):
    save_message(message)