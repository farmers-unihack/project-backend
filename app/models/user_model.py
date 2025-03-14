from bson.objectid import ObjectId


class UserModel:
    def get_user(self, user_id: str):
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user is None:
                raise ValueError("User not found")
            return user
        except ValueError as ve:
            print(f"Error getting user: {ve}")
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
