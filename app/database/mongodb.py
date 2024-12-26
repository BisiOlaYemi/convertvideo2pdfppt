from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DATABASE_NAME]
conversions = db.conversions