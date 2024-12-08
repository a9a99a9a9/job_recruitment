from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
import os


class Job:
    # MongoDB 연결 설정
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:3000/")
    collection = MongoClient(MONGO_URI)['job_crawler']['saramin_jobs']

    @classmethod
    def find_all(cls, filters=None, skip=0, limit=20):
        """
        필터와 페이지네이션을 적용하여 데이터 조회
        :param filters: 필터 조건 (dict)
        :param skip: 건너뛸 데이터 수 (페이지네이션 시작점)
        :param limit: 반환할 데이터 수 (페이지 크기)
        :return: 필터 및 페이지네이션이 적용된 데이터 리스트
        """
        filters = filters or {}
        jobs = list(cls.collection.find(filters).skip(skip).limit(limit))
        return cls.serialize_jobs(jobs)

    @classmethod
    def count(cls, filters=None):
        """
        필터 조건에 해당하는 전체 데이터 개수 반환
        :param filters: 필터 조건 (dict)
        :return: 데이터 개수 (int)
        """
        filters = filters or {}
        return cls.collection.count_documents(filters)

    @classmethod
    def save(cls, data):
        """
        채용 공고 데이터를 저장
        :param data: 저장할 데이터 (dict)
        :return: 저장된 데이터의 ID (str)
        """
        required_fields = ["title", "company", "location", "deadline"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        job_id = cls.collection.insert_one(data).inserted_id
        return str(job_id)  # ObjectId를 문자열로 반환

    @classmethod
    def update(cls, job_id, data):
        """
        특정 채용 공고를 수정
        :param job_id: 수정할 데이터의 ID (str)
        :param data: 수정할 데이터 (dict)
        :return: 수정된 문서 개수 (int)
        """
        result = cls.collection.update_one({"_id": ObjectId(job_id)}, {"$set": data})
        return result.modified_count

    @classmethod
    def delete(cls, job_id):
        """
        특정 채용 공고를 삭제
        :param job_id: 삭제할 데이터의 ID (str)
        :return: 삭제된 문서 개수 (int)
        """
        result = cls.collection.delete_one({"_id": ObjectId(job_id)})
        return result.deleted_count

    @classmethod
    def search(cls, query):
        """
        제목 또는 회사명으로 채용 공고를 검색
        :param query: 검색어 (str)
        :return: 검색된 데이터 리스트
        """
        if not query:
            return []

        search_filter = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"company": {"$regex": query, "$options": "i"}}
            ]
        }
        jobs = list(cls.collection.find(search_filter))
        return cls.serialize_jobs(jobs)

    @staticmethod
    def serialize_jobs(jobs):
        """
        MongoDB 데이터의 ObjectId를 문자열로 변환
        :param jobs: 데이터 리스트
        :return: ObjectId가 문자열로 변환된 데이터 리스트
        """
        for job in jobs:
            job['_id'] = str(job['_id'])  # ObjectId를 문자열로 변환
        return jobs


def get_job_collection():
    """
    MongoDB 컬렉션 초기화 및 인덱스 설정
    :return: MongoDB 컬렉션
    """
    client = MongoClient("mongodb://localhost:3000/")
    db = client['job_crawler']
    collection = db['saramin_jobs']

    # 인덱스 설정 (최초 호출 시 한 번만 실행 필요)
    collection.create_index([("title", ASCENDING)], name="title_index")
    collection.create_index([("company", ASCENDING)], name="company_index")
    collection.create_index([("location", ASCENDING)], name="location_index")
    collection.create_index([("deadline", ASCENDING)], name="deadline_index")
    print("Job 모델: 인덱스 설정 완료")

    return collection
