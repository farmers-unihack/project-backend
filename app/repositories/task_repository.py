from typing import Optional
from bson import ObjectId
from pymongo.database import Database
from app.models.task_model import Task
from pymongo.results import UpdateResult, DeleteResult


class TaskRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create_task(self, name: str, description: str = "") -> Optional[Task]:
        task_data = {
            "name": name,
            "description": description,
            "completion_date": None,
            "completed": False,
        }
        result = self.db.tasks.insert_one(task_data)
        if result.inserted_id is None:
            return None
        task_data["_id"] = result.inserted_id
        return Task(task_data)

    def find_task_by_id(self, task_id: str) -> Optional[Task]:
        task_data = self.db.tasks.find_one({"_id": ObjectId(task_id)})
        return Task(task_data) if task_data else None

    def update_task(self, task_id: str, update_fields: dict) -> UpdateResult:
        return self.db.tasks.update_one(
            {"_id": ObjectId(task_id)}, {"$set": update_fields}
        )

    def delete_task_by_id(self, task_id: str) -> DeleteResult:
        return self.db.tasks.delete_one({"_id": ObjectId(task_id)})
