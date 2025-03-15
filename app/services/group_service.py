import itertools
from typing import Optional
from app.models.group_model import Group
from app.models.task_model import Task
from app.repositories.group_repository import GroupRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository


class GroupService:
    def __init__(
        self,
        group_repository: GroupRepository,
        user_repository: UserRepository,
        task_repository: TaskRepository,
    ) -> None:
        self.group_repository = group_repository
        self.user_repository = user_repository
        self.task_repository = task_repository

    def create_group(self, group_name: str, user_id: str) -> Group:
        # TODO: check if the user is already in a group
        created_group = self.group_repository.create_group(group_name, user_id)
        if not created_group:
            raise ValueError("Group could not be created")
        return created_group

    def find_group_by_id(self, group_id: Optional[str]) -> Group:
        if not group_id:
            raise ValueError("GroupId was not provided")

        group = self.group_repository.find_group_by_id(group_id)
        if group is None:
            raise ValueError("Group does not exist")
        return group

    def add_user_to_group(self, group_id: str, user_id: str) -> Group:
        group = self.find_group_by_id(group_id)

        if not self.user_repository.find_by_id(user_id):
            raise ValueError("User does not exist")

        if group.get_member_count() >= Group.MAX_USERS_IN_GROUP:
            raise ValueError("Group is full")

        if group.contains_user(user_id):
            raise ValueError("User already in group")

        update_result = self.group_repository.add_user_to_group(group_id, user_id)

        if update_result.modified_count == 0:
            raise ValueError("User cannot be added to group")

        return group

    def remove_user_from_group(self, group_id: str, user_id: str) -> Group | None:
        group = self.find_group_by_id(group_id)

        if not self.user_repository.find_by_id(user_id):
            raise ValueError("User does not exist")

        if not group.contains_user(user_id):
            raise ValueError("User not in group")

        # delete the group if the user is the only member
        if group.get_member_count() == 1:
            update_result = self.group_repository.delete_group_by_id(group_id)
            if update_result.deleted_count == 0:
                raise ValueError("Group could not be deleted")
            return None

        update_result = self.group_repository.remove_user_from_group(group_id, user_id)

        if update_result.modified_count == 0:
            raise ValueError("User cannot be removed from group")

        return group

    def get_group_tasks(self, group_id: str) -> list[Task]:
        group = self.find_group_by_id(group_id)
        if not group:
            raise ValueError("Group does not exist")
        tasks = itertools.chain.from_iterable(
            map(
                lambda user_id: self.task_repository.find_tasks_by_user_id(user_id),
                group.users,
            )
        )
        return tasks
