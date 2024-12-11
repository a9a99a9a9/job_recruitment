from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
import os

class Job:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:3000/")
    collection = MongoClient(MONGO_URI)['job_crawler']['saramin_jobs']

    @classmethod
    def find_all(cls, filters=None, sort_by="created_at", order=-1, skip=0, limit=20):
        filters = filters or {}
        sort_order = DESCENDING if order == -1 else ASCENDING
        jobs = list(cls.collection.find(filters).sort(sort_by, sort_order).skip(skip).limit(limit))
        return cls.serialize_jobs(jobs)

    @classmethod
    def find_by_id(cls, job_id):
        job = cls.collection.find_one({"_id": ObjectId(job_id)})
        if job:
            job['_id'] = str(job['_id'])
        return job

    @classmethod
    def increment_views(cls, job_id):
        cls.collection.update_one({"_id": ObjectId(job_id)}, {"$inc": {"views": 1}})

    @classmethod
    def recommend_jobs(cls, job_id):
        current_job = cls.find_by_id(job_id)
        if not current_job:
            return []
        filters = {
            "$or": [
                {"company": current_job.get("company")},
                {"stack": {"$in": current_job.get("stack", [])}}
            ]
        }
        jobs = list(cls.collection.find(filters).limit(5))
        return cls.serialize_jobs(jobs)

    @classmethod
    def count(cls, filters=None):
        filters = filters or {}
        return cls.collection.count_documents(filters)

    @classmethod
    def search(cls, query):
        if not query:
            return []
        search_filter = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"company": {"$regex": query, "$options": "i"}},
                {"stack": {"$regex": query, "$options": "i"}},
            ]
        }
        jobs = list(cls.collection.find(search_filter))
        return cls.serialize_jobs(jobs)

    @staticmethod
    def serialize_jobs(jobs):
        for job in jobs:
            job['_id'] = str(job['_id'])
        return jobs
