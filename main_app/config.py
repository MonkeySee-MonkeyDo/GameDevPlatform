from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")