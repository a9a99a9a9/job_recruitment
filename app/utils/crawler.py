import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import logging
import time
from concurrent.futures import ThreadPoolExecutor

# 로깅 설정
logging.basicConfig(filename='crawler_errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s')


# MongoDB 연결 설정
def connect_to_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['job_crawler']
    collection = db['saramin_jobs']

    # 고유 인덱스 설정 (중복 방지)
    collection.create_index("링크", unique=True)
    print("MongoDB에 연결되었습니다! (고유 인덱스 설정 완료)")

    return collection


# 크롤링 실패 복구 로직 (재시도)
def crawl_page_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"시도 {attempt + 1}/{max_retries} 실패: {e}")
            time.sleep(2)  # 재시도 간 딜레이
    logging.error(f"{url} 페이지 크롤링 실패!")
    return None


# 단일 페이지 크롤링 함수
def crawl_page(keyword, page, headers):
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
    response = crawl_page_with_retry(url, headers)
    if response is None:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select('.item_recruit')


# 병렬 처리로 크롤링
def crawl_saramin(keyword, pages=1):
    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(crawl_page, keyword, page, headers) for page in range(1, pages + 1)]
        for future in futures:
            job_listings = future.result()
            for job in job_listings:
                try:
                    # 데이터 추출
                    company = job.select_one('.corp_name a').text.strip()
                    title = job.select_one('.job_tit a').text.strip()
                    link = 'https://www.saramin.co.kr' + job.select_one('.job_tit a')['href']
                    conditions = job.select('.job_condition span')
                    location = conditions[0].text.strip() if len(conditions) > 0 else ''
                    experience = conditions[1].text.strip() if len(conditions) > 1 else ''
                    education = conditions[2].text.strip() if len(conditions) > 2 else ''
                    employment_type = conditions[3].text.strip() if len(conditions) > 3 else ''
                    deadline = job.select_one('.job_date .date').text.strip()
                    job_sector = job.select_one('.job_sector')
                    sector = job_sector.text.strip() if job_sector else ''
                    salary_badge = job.select_one('.area_badge .badge')
                    salary = salary_badge.text.strip() if salary_badge else ''

                    jobs.append({
                        '회사명': company,
                        '제목': title,
                        '링크': link,
                        '지역': location,
                        '경력': experience,
                        '학력': education,
                        '고용형태': employment_type,
                        '마감일': deadline,
                        '직무분야': sector,
                        '연봉정보': salary
                    })

                except AttributeError as e:
                    logging.error(f"항목 파싱 중 에러 발생: {e}")
                    continue

    print(f"크롤링 완료, 총 {len(jobs)}개의 채용공고 수집")
    return pd.DataFrame(jobs)


# MongoDB에 데이터 저장
def save_to_mongodb(dataframe):
    collection = connect_to_mongodb()
    records = dataframe.to_dict(orient='records')
    inserted_count = 0

    for record in records:
        try:
            collection.insert_one(record)  # 중복 데이터 방지 (고유 인덱스 덕분에 에러 발생)
            inserted_count += 1
        except Exception as e:
            if "duplicate key error" in str(e):
                print(f"중복 데이터 건너뜀: {record['링크']}")
            else:
                logging.error(f"데이터 삽입 중 에러 발생: {e}")

    print(f"{inserted_count}개의 새로운 채용공고가 MongoDB에 저장되었습니다!")
