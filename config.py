import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "gemini_chatbot")

    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    @staticmethod
    def validate():
        required = {
            "GEMINI_API_KEY": Config.GEMINI_API_KEY,
            "MONGO_URI": Config.MONGO_URI,
            "DATABASE_NAME": Config.DATABASE_NAME,
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
