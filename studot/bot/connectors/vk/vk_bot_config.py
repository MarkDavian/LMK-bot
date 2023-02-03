from vkbottle import BuiltinStateDispenser, ABCStateDispenser
from vkbottle.dispatch.dispenser.base import StatePeer
from vkbottle.bot import BotLabeler

from bot.core.utils.db.db import database


class MongoStateDispenser(ABCStateDispenser):
    def __init__(self):
        self.db = database['vk_states']

    async def get(self, peer_id: int):
        r = self.db.find_one(
            {'peer_id': peer_id}
        )
        if r is None:
            return None
        r.pop('_id')
        return StatePeer(**r)

    async def set(self, peer_id: int, state, **payload):
        peer = StatePeer(peer_id=peer_id, state=state, payload=payload)
        r = self.db.find_one(
            {'peer_id': peer_id}
        )
        if r is None:
            self.db.insert_one(
                peer.dict()
            )
        else:
            self.db.update_one(
                {'peer_id': peer_id},
                {'$set': {**peer.dict()}}
            )

    async def delete(self, peer_id: int):
        self.db.delete_one(
            {'peer_id': peer_id}
        )


labeler = BotLabeler()
labeler.vbml_ignore_case = True
state_dispenser = MongoStateDispenser()
