
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from config import Config

class MongoDB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)

        # Explicitly select the database
        self.db = self.client[Config.DATABASE_NAME]

        self.chats = self.db["chats"]
    def create_chat(self):
        """Create a new empty chat."""
        now = datetime.now()

        chat = {
        "title": "",  # Will be updated with first message
        "created_at": now,
        "updated_at": now,
        "messages": []
        }

        result = self.chats.insert_one(chat)
        chat["_id"] = str(result.inserted_id)

        return chat

    def get_all_chats(self):
        """Return all chats sorted by newest first."""
        chats = []

        for chat in self.chats.find().sort("created_at", -1):
            chats.append({
                "_id": str(chat["_id"]),
                "title": chat["title"],
                "created_at": chat["created_at"],
                "updated_at": chat["updated_at"]
            })

        return chats

    def get_chat(self, chat_id):
        """Get a single chat by ID."""
        chat = self.chats.find_one({"_id": ObjectId(chat_id)})

        if not chat:
            return None

        chat["_id"] = str(chat["_id"])
        return chat

    def add_message(self, chat_id, role, content):
        """Add a message to an existing chat."""

        chat = self.chats.find_one({"_id": ObjectId(chat_id)})

        if not chat:
            return False

        update = {
            "$push": {
            "messages": {
                "role": role,
                "content": content
            }
        },
        "$set": {
            "updated_at": datetime.now()
        }
    }

    # If this is the first message, use it as the title
        if len(chat["messages"]) == 0:
            update["$set"]["title"] = content[:50]  # limit title length

        self.chats.update_one(
            {"_id": ObjectId(chat_id)},
            update
        )

        return True

    def delete_chat(self, chat_id):
        """Delete a chat."""
        result = self.chats.delete_one(
            {"_id": ObjectId(chat_id)}
        )

        return result.deleted_count > 0

