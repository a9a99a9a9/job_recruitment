from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client['job_crawler']
collection = db['saramin_jobs']

# 블루프린트 생성
job_routes = Blueprint('job_routes', __name__)

# GET /jobs - 모든 채용 공고 조회 (페이지네이션, 필터링, 정렬)
@job_routes.route('/jobs', methods=['GET'])
def get_jobs():
    # 쿼리 매개변수 처리
    page = int(request.args.get('page', 1))  # 기본값: 1페이지
    limit = int(request.args.get('limit', 20))  # 기본값: 페이지당 20개
    skip = (page - 1) * limit  # 스킵할 문서 수 계산
    sort_by = request.args.get('sort_by', '마감일')  # 기본 정렬 필드: 마감일
    sort_order = request.args.get('sort_order', 'asc')  # 기본 정렬 순서: 오름차순
    filters = {}

    # 필터링 조건 처리
    company = request.args.get('company')  # 회사명
    location = request.args.get('location')  # 지역
    experience = request.args.get('experience')  # 경력
    job_title = request.args.get('title')  # 채용 제목

    if company:
        filters['회사명'] = {'$regex': company, '$options': 'i'}  # 대소문자 구분 없이 검색
    if location:
        filters['지역'] = {'$regex': location, '$options': 'i'}
    if experience:
        filters['경력'] = {'$regex': experience, '$options': 'i'}
    if job_title:
        filters['제목'] = {'$regex': job_title, '$options': 'i'}

    # 정렬 설정
    sort_order = 1 if sort_order == 'asc' else -1  # asc는 1, desc는 -1
    jobs = list(
        collection.find(filters)
        .sort(sort_by, sort_order)
        .skip(skip)
        .limit(limit)
    )

    # ObjectId 문자열 변환
    for job in jobs:
        job['_id'] = str(job['_id'])

    # 총 문서 수 계산
    total_items = collection.count_documents(filters)

    # 응답 반환
    return jsonify({
        'status': 'success',
        'data': jobs,
        'pagination': {
            'currentPage': page,
            'limit': limit,
            'totalItems': total_items,
            'totalPages': (total_items // limit) + (1 if total_items % limit > 0 else 0),
        }
    })

# GET /jobs/all - 모든 채용 공고 조회 (필터링만, 페이지네이션 없음)
@job_routes.route('/jobs/all', methods=['GET'])
def get_all_jobs():
    filters = {}

    # 필터링 조건 처리
    company = request.args.get('company')  # 회사명
    location = request.args.get('location')  # 지역
    experience = request.args.get('experience')  # 경력
    job_title = request.args.get('title')  # 채용 제목

    if company:
        filters['회사명'] = {'$regex': company, '$options': 'i'}  # 대소문자 구분 없이 검색
    if location:
        filters['지역'] = {'$regex': location, '$options': 'i'}
    if experience:
        filters['경력'] = {'$regex': experience, '$options': 'i'}
    if job_title:
        filters['제목'] = {'$regex': job_title, '$options': 'i'}

    # 모든 데이터 조회
    jobs = list(collection.find(filters))
    for job in jobs:
        job['_id'] = str(job['_id'])

    # 응답 반환
    return jsonify({
        'status': 'success',
        'data': jobs,
        'totalItems': len(jobs)
    })
