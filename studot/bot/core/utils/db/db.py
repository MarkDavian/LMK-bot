# import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings


client = AsyncIOMotorClient(
    settings.mongo_host,
    settings.mongo_port
)

database = client['main']
collection = database['users']