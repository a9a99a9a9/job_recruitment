from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Application:
    client = MongoClient("mongodb://localhost:3000/")
    db = client['job_crawler']
    collection = db['applications']

    @classmethod
    def initialize_indexes(cls):
        cls.collection.create_index([("user_id", ASCENDING), ("job_id", ASCENDING)], unique=True)
        cls.collection.create_index("created_at", DESCENDING)
        print("Application 모델: 인덱스 설정 완료")

    @classmethod
    def apply(cls, user_id, job_id, resume=None):
        if cls.collection.find_one({"user_id": user_id, "job_id": job_id}):
            raise ValueError("이미 지원한 공고입니다.")
        application = {
            "user_id": user_id,
            "job_id": job_id,
            "resume": resume,
            "status": "pending",
            "created_at": datetime.now(timezone.utc)
        }
        return cls.collection.insert_one(application).inserted_id

    @classmethod
    def find_by_user(cls, user_id, filters=None, sort_by="created_at", order=-1):
        query = {"user_id": user_id}
        if filters:
            query.update(filters)
        sort_order = DESCENDING if order == -1 else ASCENDING
        return list(cls.collection.find(query).sort(sort_by, sort_order))

    @classmethod
    def cancel(cls, application_id):
        application = cls.collection.find_one({"_id": ObjectId(application_id)})
        if not application or application["status"] != "pending":
            raise ValueError("취소할 수 없는 상태입니다.")
        return cls.collection.update_one({"_id": ObjectId(application_id)}, {"$set": {"status": "canceled"}}).modified_count

    @classmethod
    def update_status(cls, application_id, status):
        return cls.collection.update_one({"_id": ObjectId(application_id)}, {"$set": {"status": status}}).modified_count
