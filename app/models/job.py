from pymongo import MongoClient, ASCENDING

from bson.objectid import ObjectId

class Job:
    collection = MongoClient("mongodb://localhost:27017/")['job_crawler']['jobs']

    @classmethod
    def find_all(cls, filters=None):
        filters = filters or {}
        return list(cls.collection.find(filters))

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data).inserted_id

    @classmethod
    def update(cls, job_id, data):
        return cls.collection.update_one({"_id": ObjectId(job_id)}, {"$set": data}).modified_count

    @classmethod
    def delete(cls, job_id):
        return cls.collection.delete_one({"_id": ObjectId(job_id)}).deleted_count

    @classmethod
    def search(cls, query):
        return list(cls.collection.find({"title": {"$regex": query, "$options": "i"}}))


def get_job_collection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['job_crawler']
    collection = db['jobs']

    # 인덱스 설정 (탐색 최적화)
    collection.create_index("title", ASCENDING)
    collection.create_index("company", ASCENDING)
    collection.create_index("location", ASCENDING)
    collection.create_index("deadline", ASCENDING)
    print("Job 모델: 인덱스 설정 완료")

    return collection
