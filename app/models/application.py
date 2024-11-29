from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId

class Application:
    collection = MongoClient("mongodb://localhost:27017/")['job_crawler']['applications']

    @classmethod
    def apply(cls, user_id, job_id):
        return cls.collection.insert_one({"user_id": user_id, "job_id": job_id}).inserted_id

    @classmethod
    def find_by_user(cls, user_id):
        return list(cls.collection.find({"user_id": user_id}))

    @classmethod
    def cancel(cls, application_id):
        return cls.collection.delete_one({"_id": ObjectId(application_id)}).deleted_count

def get_application_collection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['job_crawler']
    collection = db['applications']

    # 인덱스 설정 (사용자와 공고 간의 관계)
    collection.create_index([("user_id", ASCENDING), ("job_id", ASCENDING)], unique=True)
    print("Application 모델: 인덱스 설정 완료")

    return collection
