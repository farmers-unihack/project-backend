from typing import Any


class Collectible:
    PER_COLLECTIBLE_TIME_INCREMENT = 5 * 3500 # in seconds

    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data["_id"]
        self.name = data["name"]
        self.description = data["description"]
        self.image_url = data["image_url"]
