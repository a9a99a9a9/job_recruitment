from pymongo import MongoClient
import os

client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
db = client.job_crawler  # 데이터베이스 이름

# 각 모델에서 사용할 수 있도록 db를 export
__all__ = ['db']
