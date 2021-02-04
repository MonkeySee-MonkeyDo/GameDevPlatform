from dotenv import load_dotenv
import os

load_dotenv()

username=os.getenv("MONGO_USERNAME")
password=os.getenv("MONGO_PASSWORD")
cluster_url=os.getenv("MONGO_CLUSTER_URL")
db=os.getenv("MONGO_DB")

class Config:
    MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster_url}/{db}?retryWrites=true&w=majority"