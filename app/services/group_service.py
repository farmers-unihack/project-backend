from typing import Optional
from app.models.group_model import Group
from app.repositories import user_repository
from app.repositories.group_repository import GroupRepository
from app.repositories.user_repository import UserRepository

class GroupService:
    def __init__(self, group_repository: GroupRepository, user_repository: UserRepository) -> None:
        self.group_repository = group_repository
        self.user_repository = user_repository

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

        if group.get_member_count() == 1:
            # TODO handle group deletion if last member leaves
            pass

        self.group_repository.remove_user_from_group(group_id, user_id)
        return (True, "User remove from group")
