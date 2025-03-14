from bson.objectid import ObjectId
from pymongo.collection import Collection

from app import get_db
from app.utils.time import get_current_time


class TaskModel:
    def __init__(self):
        self.collection: Collection = get_db().tasks

    def create_task(self, name: str, description: str = ""):
        task = {
            "name": name,
            "description": description,
            "completion_date": None,
            "completed": False,
        }
        result = self.collection.insert_one(task)
        return result.inserted_id

    def get_task(self, task_id: str):
        try:
            return self.collection.find_one({"_id": ObjectId(task_id)})
        except Exception as e:
            print(f"Error getting task: {e}")
            return None

    def update_task(
        self,
        task_id: str,
        name: str = None,
        description: str = None,
        completed: bool = None,
    ):
        update_fields = {}
        if name:
            update_fields["name"] = name
        if description:
            update_fields["description"] = description
        if completed is not None:
            update_fields["completed"] = completed
            update_fields["completion_date"] = get_current_time() if completed else None
        if update_fields:
            try:
                updated = self.collection.update_one(
                    {"_id": ObjectId(task_id)}, {"$set": update_fields}
                )
                if updated.modified_count == 0:
                    raise ValueError("Task not found")
            except ValueError as ve:
                print(f"Error updating task: {ve}")
            except Exception as e:
                print(f"Unexpected error updating task: {e}")

    def delete_task(self, task_id: str):
        try:
            self.collection.delete_one({"_id": ObjectId(task_id)})
        except Exception as e:
            print(f"Error deleting task: {e}")
