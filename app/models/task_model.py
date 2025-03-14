from datetime import timedelta
from bson.objectid import ObjectId
from app.utils.time import get_current_time
from app.extensions import get_db

class TaskModel:
    @staticmethod
    def create_task(name: str, description: str = ""):
        task = {
            "name": name,
            "description": description,
            "completion_date": None,
            "completed": False,
        }
        result = get_db().insert_one(task)
        return result.inserted_id

    @staticmethod
    def get_task(task_id: str):
        try:
            return get_db().find_one({"_id": ObjectId(task_id)})
        except Exception as e:
            print(f"Error getting task: {e}")
            return None

    @staticmethod
    def update_task(
        TaskModel,
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
                updated = get_db().update_one(
                    {"_id": ObjectId(task_id)}, {"$set": update_fields}
                )
                if updated.modified_count == 0:
                    raise ValueError("Task not found")
            except ValueError as ve:
                print(f"Error updating task: {ve}")
            except Exception as e:
                print(f"Unexpected error updating task: {e}")

    @staticmethod
    def delete_task(task_id: str):
        try:
            get_db().delete_one({"_id": ObjectId(task_id)})
        except Exception as e:
            print(f"Error deleting task: {e}")

    @staticmethod
    def is_task_completed_within_recent_time(task_id: str, time_limit: timedelta):
        task = TaskModel.get_task(task_id)
        return (
            task["completed"]
            and get_current_time() - task["completion_time"] < time_limit
            if task
            else None
        )
