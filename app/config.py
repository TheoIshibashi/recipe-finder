from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MEALDB_API_KEY = os.getenv("MEALDB_API_KEY", default="1")
    PROJECT_NAME = os.getenv("PROJECT_NAME", default="Recipe Finder")

settings = Settings()