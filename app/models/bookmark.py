from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Bookmark:
    collection = MongoClient("mongodb://localhost:3000/")['job_crawler']['bookmarks']

    @classmethod
    def toggle(cls, user_id, job_id):
        """
        북마크 토글 처리: 존재하면 삭제, 존재하지 않으면 추가
        """
        existing_bookmark = cls.collection.find_one({"user_id": user_id, "job_id": job_id})
        if existing_bookmark:
            cls.collection.delete_one({"_id": existing_bookmark["_id"]})
            return "deleted"
        else:
            bookmark = {
                "user_id": user_id,
                "job_id": job_id,
                "created_at": datetime.now(timezone.utc),
            }
            cls.collection.insert_one(bookmark)
            return "added"

    @classmethod
    def find_by_user(cls, user_id, skip=0, limit=20):
        """
        사용자별 북마크 조회 (페이지네이션 및 최신순 정렬)
        """
        bookmarks = list(
            cls.collection.find({"user_id": user_id})
            .sort("created_at", DESCENDING)
            .skip(skip)
            .limit(limit)
        )
        return cls.serialize_bookmarks(bookmarks)

    @classmethod
    def count(cls, user_id):
        """
        사용자별 북마크 총 개수 반환
        """
        return cls.collection.count_documents({"user_id": user_id})

    @staticmethod
    def serialize_bookmarks(bookmarks):
        """
        북마크 데이터를 직렬화 (ObjectId 변환)
        """
        for bookmark in bookmarks:
            bookmark["_id"] = str(bookmark["_id"])
        return bookmarks
