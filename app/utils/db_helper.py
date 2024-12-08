from pymongo import MongoClient

def connect_to_db():
    client = MongoClient("mongodb://localhost:3000/")
    db = client['job_crawler']
    return db
