from typing import Optional
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import UpdateResult
from pymongo.results import DeleteResult

from app.models.collectible_model import Collectible


class CollectibleRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def find_random_collectible_excluding(self, exclude_id_list: list[str]) -> Optional[Collectible]:
        # TODO: maybe we want this to be based on some chance? Like gacha?
        pipeline = [
            {"$match": {"_id": {"$nin": [ObjectId(_id) for _id in exclude_id_list]}}},
            {"$sample": {"size": 1}}
        ]
        result = list(self.db.collectibles.aggregate(pipeline))
        return Collectible(result[0]) if result else None

    def find_by_id(self, collectible_id: str) -> Optional[Collectible]:
        collectible_data = self.db.collectibles.find_one(
            {"_id": ObjectId(collectible_id)}
        )
        return Collectible(collectible_data) if collectible_data else None
