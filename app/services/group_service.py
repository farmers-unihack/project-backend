from app.repositories.group_repository import GroupRepository

class GroupService:
    def __init__(self, group_repository: GroupRepository) -> None:
        self.group_repository = group_repository
