from dotenv import load_dotenv
import os

load_dotenv()

username=os.getenv("MONGO_USERNAME")
password=os.getenv("MONGO_PASSWORD")
cluster_url=os.getenv("MONGO_CLUSTER_URL")
db=os.getenv("MONGO_DB")
secret_key=os.getenv("SECRET_KEY")

class Config:
    MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster_url}/{db}?retryWrites=true&w=majority"
    SECRET_KEY = secret_key