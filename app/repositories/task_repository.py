from pymongo.database import Database

class TaskRepository:
    def __init__(self, db: Database) -> None:
        self.db = db
