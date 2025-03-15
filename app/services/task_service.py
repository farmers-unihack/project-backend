from datetime import timedelta
from typing import Optional
from app.models.task_model import Task
from app.repositories.task_repository import TaskRepository
from app.utils.time import get_current_time


class TaskService:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def create_task(self, name: str, description: str = "") -> Task:
        result = self.task_repository.create_task(name, description)
        if result is None:
            raise ValueError("Task could not be created")
        return result

    def find_task_by_id(self, task_id: str) -> Task:
        task = self.task_repository.find_task_by_id(task_id)
        if task is None:
            raise ValueError("Task does not exist")
        return task

    def update_task(
        self,
        task_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> None:
        update_fields = {}
        if name:
            update_fields["name"] = name

        if description:
            update_fields["description"] = description

        if completed is not None:
            update_fields["completed"] = completed
            update_fields["completion_date"] = get_current_time() if completed else None

        if not update_fields:
            raise ValueError("No update fields provided")

        update_result = self.task_repository.update_task(task_id, update_fields)
        if update_result.modified_count == 0:
            raise ValueError("Task could not be updated")

    def delete_task(self, task_id: str) -> None:
        delete_result = self.task_repository.delete_task_by_id(task_id)
        if delete_result.deleted_count == 0:
            raise ValueError("Task could not be deleted")
        return None

    def is_task_completed_within_recent_time(self, task_id: str, time_limit: timedelta):
        task = self.find_task_by_id(task_id)
        return task.is_completed_within_recent_time(time_limit)
