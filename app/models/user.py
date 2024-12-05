from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

class User:
    # MongoDB 연결 및 컬렉션 초기화
    client = MongoClient("mongodb://localhost:3000/")
    db = client['job_crawler']
    collection = db['users']

    # 초기화 시 인덱스 설정
    @classmethod
    def initialize_indexes(cls):
        cls.collection.create_index("email", unique=True)
        cls.collection.create_index("username", unique=True)
        print("User 모델: 인덱스 설정 완료")

    # 사용자 생성
    def __init__(self, email, password, username=None):
        self.email = email
        self.password = password
        self.username = username

    def save(self):
        try:
            user_data = {
                "email": self.email,
                "password": self.password,
                "username": self.username,
            }
            result = self.collection.insert_one(user_data)
            return result.inserted_id
        except DuplicateKeyError as e:
            raise ValueError("중복된 이메일 또는 사용자 이름이 존재합니다.") from e

    @classmethod
    def find_by_email(cls, email):
        return cls.collection.find_one({"email": email})

    @classmethod
    def find_by_id(cls, user_id):
        return cls.collection.find_one({"_id": ObjectId(user_id)})

    @classmethod
    def update(cls, user_id, data):
        result = cls.collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        return result.modified_count

    @classmethod
    def delete(cls, user_id):
        result = cls.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count


# 인덱스 초기화 (스크립트 실행 시 단 한 번 실행)
User.initialize_indexes()