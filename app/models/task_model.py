from bson.objectid import ObjectId
from app import get_db
from pymongo.collection import Collection

class TaskModel:
    def __init__(self):
        self.collection: Collection = get_db().tasks

    def create_task(self, name, description):
        task = {
            "name": name,
            "description": description,
        }
        result = self.collection.insert_one(task)
        return result.inserted_id

    def get_task(self, task_id):
        try:
            return self.collection.find_one({"_id": ObjectId(task_id)})
        except Exception as e:
            print(f"Error getting task: {e}")
            return None

    def update_task(self, task_id, title=None, description=None):
        update_fields = {}
        if title:
            update_fields["title"] = title
        if description:
            update_fields["description"] = description
        if update_fields:
            try:
                self.collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_fields})
            except Exception as e:
                print(f"Error updating task: {e}")

    def delete_task(self, task_id):
        try:
            self.collection.delete_one({"_id": ObjectId(task_id)})
        except Exception as e:
            print(f"Error deleting task: {e}")

    def get_all_tasks(self):
        try:
            return list(self.collection.find())
        except Exception as e:
            print(f"Error getting all tasks: {e}")
            return []