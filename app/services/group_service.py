import itertools
import random
from typing import Iterable, Optional
from app.models.group_model import Group
from app.models.task_model import Task
from app.repositories.group_repository import GroupRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.static.collectibles import ALL_COLLECTIBLES


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

    def create_group(self, group_name: str, user_id: str) -> None:
        if self.is_user_in_group(user_id):
            raise ValueError("User is already in a group")

        if not self.group_repository.create_group(group_name, user_id):
            raise ValueError("Group could not be created")

    def find_group_by_id(self, group_id: Optional[str]) -> Group:
        if not group_id:
            raise ValueError("GroupId was not provided")

        group = self.group_repository.find_group_by_id(group_id)
        if group is None:
            raise ValueError("Group does not exist")
        return group

    def is_user_in_group(self, user_id: str) -> bool:
        try:
            self.find_group_by_user_id(user_id)
            return True
        except:
            return False

    def find_group_by_user_id(self, user_id: str) -> Group:
        group = self.group_repository.find_group_by_user_id(user_id)
        if group is None:
            raise ValueError(f"Group with user {user_id} does not exist")
        return group

    def add_user_by_invite(self, invite_code: str, user_id: str) -> Group:
        group_id = self.group_repository.find_group_by_invite_code(invite_code)
        if not group_id:
            raise ValueError(f"Group with invite code {invite_code} does not exist")
        return self.add_user_to_group(group_id, user_id)

    def add_user_to_group(self, group_id: str, user_id: str) -> Group:
        if self.is_user_in_group(user_id):
            raise ValueError("User is already in a group")

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

    def remove_user_from_group(self, user_id: str) -> None:
        group = self.find_group_by_user_id(user_id)

        # delete the group if the user is the only member
        if group.get_member_count() == 1:
            update_result = self.group_repository.delete_group_by_id(group.id)
            if update_result.deleted_count == 0:
                raise ValueError("Group could not be deleted")
        else:
            update_result = self.group_repository.remove_user_from_group(
                group.id, user_id
            )
            if update_result.modified_count == 0:
                raise ValueError("User cannot be removed from group")

    def get_group_tasks(self, current_usere_id: str) -> Iterable[Task]:
        group = self.find_group_by_user_id(current_usere_id)
        if not group:
            raise ValueError("Group does not exist")
        tasks = itertools.chain.from_iterable(
            map(
                lambda user_id: self.task_repository.find_tasks_by_user_id(user_id),
                group.users,
            )
        )
        return tasks

    def add_random_collectible_to_group(self, current_user_id: str):
        group = self.find_group_by_user_id(current_user_id)
        if not group:
            raise ValueError("Group does not exist")
        # find one that is not owned by the group
        collectible_name = random.choice(
            [
                key
                for key in ALL_COLLECTIBLES.keys()
                if key not in set(group.collectibles)
            ]
        )
        if len(group.collectibles) == len(ALL_COLLECTIBLES):
            # FIXME this should be a log
            print("No more collectibles to add")
            return
        update_result = self.group_repository.add_collectible_to_group(
            group.id, collectible_name
        )
        if update_result.modified_count == 0:
            raise ValueError("Collectible cannot be added to group")
        return
