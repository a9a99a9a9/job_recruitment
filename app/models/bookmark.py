from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId

class Bookmark:
    collection = MongoClient("mongodb://localhost:3000/")['job_crawler']['bookmarks']

    @classmethod
    def add(cls, user_id, job_id):
        return cls.collection.insert_one({"user_id": user_id, "job_id": job_id}).inserted_id

    @classmethod
    def find_by_user(cls, user_id):
        return list(cls.collection.find({"user_id": user_id}))

    @classmethod
    def delete(cls, bookmark_id):
        return cls.collection.delete_one({"_id": ObjectId(bookmark_id)}).deleted_count

def get_bookmark_collection():
    client = MongoClient("mongodb://localhost:3000/")
    db = client['job_crawler']
    collection = db['bookmarks']

    # 인덱스 설정 (사용자와 북마크 관계)
    collection.create_index([("user_id", ASCENDING), ("job_id", ASCENDING)], unique=True)
    print("Bookmark 모델: 인덱스 설정 완료")

    return collection
