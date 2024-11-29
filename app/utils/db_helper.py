from pymongo import MongoClient

def connect_to_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['job_crawler']
    return db
