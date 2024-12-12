from flask import Blueprint, request, jsonify
from app.models.job import Job
import logging

job_routes = Blueprint('jobs', __name__)

# 채용 공고 목록 조회
@job_routes.route('/', methods=['GET'])
def get_jobs():
    filters = {key: value for key, value in request.args.items()}

    # 기본값 설정: page=1, limit=20
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    skip = (page - 1) * limit  # 현재 페이지에서 건너뛸 항목 수
    sort_by = request.args.get('sort_by', "마감일")  # 기본값 '마감일'
    order = int(request.args.get('order', -1))  # 기본값 -1 (내림차순)

    # 필터링 조건
    if '지역' in filters:
        filters['지역'] = {"$regex": filters['지역'], "$options": "i"}
    if '경력' in filters:
        filters['경력'] = {"$regex": filters['경력'], "$options": "i"}
    if '급여' in filters and filters['급여'].isdigit():  # 급여 필터가 숫자인 경우만 처리
        filters['급여'] = {"$gte": int(filters['급여'])}
    if '직무분야' in filters:
        filters['직무분야'] = {"$in": filters['직무분야'].split(",")}

    # 필터 로깅
    logging.debug(f"Filters applied: {filters}")

    # 데이터 조회
    jobs = Job.find_all(filters, sort_by=sort_by, order=order, skip=skip, limit=limit)
    total_jobs = Job.count(filters)

    # total_jobs 로깅
    logging.debug(f"Total jobs count: {total_jobs}")

    # total_jobs가 0일 경우 total_pages를 1로 설정
    total_pages = (total_jobs + limit - 1) // limit if total_jobs > 0 else 1

    # 만약 필터링된 데이터가 없다면, 필터를 비워두고 기본 데이터를 반환
    if not jobs and filters:
        logging.debug("No jobs found with current filters, fetching all jobs without filters.")
        jobs = Job.find_all({}, sort_by=sort_by, order=order, skip=skip, limit=limit)
        total_jobs = Job.count()  # 필터 없이 전체 데이터 수를 다시 계산

    response = {
        "status": "success",
        "data": jobs,
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_jobs,
            "itemsPerPage": limit,
        },
    }
    return jsonify(response), 200

# 채용 공고 상세 조회
@job_routes.route('/<job_id>', methods=['GET'])
def get_job_detail(job_id):
    job = Job.find_by_id(job_id)
    if not job:
        return jsonify({
            "status": "error",
            "message": "채용 공고를 찾을 수 없습니다.",
            "code": "JOB_NOT_FOUND"
        }), 404

    Job.increment_views(job_id)
    recommended = Job.recommend_jobs(job_id)

    return jsonify({
        "status": "success",
        "data": job,
        "recommended": recommended,
    }), 200

# 채용 공고 검색
@job_routes.route('/search', methods=['GET'])
def search_jobs():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({
            "status": "error",
            "message": "검색어가 제공되지 않았습니다.",
            "code": "MISSING_QUERY"
        }), 400

    jobs = Job.search(query)
    return jsonify({
        "status": "success",
        "data": jobs
    }), 200
