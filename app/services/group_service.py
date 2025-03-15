from typing import Optional
from app.models.group_model import Group
from app.repositories.group_repository import GroupRepository
from app.repositories.user_repository import UserRepository


class GroupService:
    def __init__(
        self, group_repository: GroupRepository, user_repository: UserRepository
    ) -> None:
        self.group_repository = group_repository
        self.user_repository = user_repository

    def create_group(self, group_name: str, user_id: str) -> Optional[Group]:
        # TODO: check if the user is already in a group
        return self.group_repository.create_group(group_name, user_id)

    def add_user_to_group(self, group_id: str, user_id: str) -> tuple[bool, str]:
        group = self.group_repository.find_group_by_id(group_id)

        if not group:
            return (False, "Group does not exist")

        if not self.user_repository.find_by_id(user_id):
            return (False, "User does not exist")

        if group.get_member_count() >= Group.MAX_USERS_IN_GROUP:
            return (False, "Group is full")

        self.group_repository.add_user_to_group(group_id, user_id)
        return (True, "User added to group")

    def remove_user_from_group(self, group_id: str, user_id: str) -> tuple[bool, str]:
        group = self.group_repository.find_group_by_id(group_id)

        if not group:
            return (False, "Group does not exist")

        if not self.user_repository.find_by_id(user_id):
            return (False, "User does not exist")

        if group.get_member_count() == 1 and group.contains_user(user_id):
            self.group_repository.delete_group_by_id(group_id)
            return (True, "Group deleted as last member left")

        delete_result = self.group_repository.remove_user_from_group(group_id, user_id)
        if delete_result.modified_count == 0:
            return (False, "User not in group")
        return (True, "User remove from group")
