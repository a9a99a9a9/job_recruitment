from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
import os

class Job:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    collection = MongoClient(MONGO_URI)['job_crawler']['saramin_jobs']

    @classmethod
    def find_all(cls, filters=None):
        filters = filters or {}
        jobs = list(cls.collection.find(filters))
        return cls.serialize_jobs(jobs)

    @classmethod
    def save(cls, data):
        required_fields = ["title", "company", "location", "deadline"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        job_id = cls.collection.insert_one(data).inserted_id
        return str(job_id)  # return string version of ObjectId

    @classmethod
    def update(cls, job_id, data):
        result = cls.collection.update_one({"_id": ObjectId(job_id)}, {"$set": data})
        return result.modified_count

    @classmethod
    def delete(cls, job_id):
        result = cls.collection.delete_one({"_id": ObjectId(job_id)})
        return result.deleted_count

    @classmethod
    def search(cls, query):
        if not query:
            return []

        search_filter = {"$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"company": {"$regex": query, "$options": "i"}}
        ]}
        jobs = list(cls.collection.find(search_filter))
        return cls.serialize_jobs(jobs)

    @staticmethod
    def serialize_jobs(jobs):
        """ Convert MongoDB's ObjectId to string """
        for job in jobs:
            job['_id'] = str(job['_id'])  # Convert ObjectId to string
        return jobs


def get_job_collection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['job_crawler']
    collection = db['saramin_jobs']

    # 인덱스 설정 (최초 호출 시 한 번만 실행 필요)
    collection.create_index([("title", ASCENDING)], name="title_index")
    collection.create_index([("company", ASCENDING)], name="company_index")
    collection.create_index([("location", ASCENDING)], name="location_index")
    collection.create_index([("deadline", ASCENDING)], name="deadline_index")
    print("Job 모델: 인덱스 설정 완료")

    return collection
