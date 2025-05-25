import os
import json
import time
import requests
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor
import math
from config import (
    COOKIES, HEADERS, ARTICLES_DIR, ARTICLES_PER_PAGE,
    REQUEST_DELAY, LOG_FILE, BASE_URL, DEFAULT_PARAMS
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# 매물 데이터를 저장할 디렉토리를 Path 객체로 변환
ARTICLES_DIR_PATH = Path(ARTICLES_DIR)

def find_complex_files():
    """data/complexes 디렉토리에서 모든 complex JSON 파일 찾기"""
    complex_files = []
    base_dir = Path("data/complexes")
    
    for city_dir in base_dir.iterdir():
        if city_dir.is_dir():
            for district_dir in city_dir.iterdir():
                if district_dir.is_dir():
                    for file_path in district_dir.glob("*_complexes.json"):
                        complex_files.append(file_path)
    
    return complex_files

def get_complexes_from_file(file_path):
    """주어진 파일에서 complex 정보 추출"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('complexList', [])

def fetch_articles(complex_no, page=1):
    """특정 단지의 매물 정보를 페이지 단위로 가져오기"""
    url = f'{BASE_URL}/{complex_no}'
    
    # 기본 파라미터 복사 후 페이지와 단지번호 추가
    params = DEFAULT_PARAMS.copy()
    params.update({
        'page': str(page),
        'complexNo': str(complex_no)
    })
    
    try:
        response = requests.get(url, params=params, cookies=COOKIES, headers=HEADERS)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"단지 {complex_no} 페이지 {page} 요청 중 오류 발생: {e}")
        return None
    except json.JSONDecodeError:
        logging.error(f"단지 {complex_no} 페이지 {page} 응답을 JSON으로 파싱할 수 없음")
        return None

def save_articles(complex_no, articles, city, district, dong):
    """매물 정보를 파일로 저장"""
    # 저장 경로 생성
    save_dir = ARTICLES_DIR_PATH / city / district / dong
    save_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = save_dir / f"{complex_no}_articles.json"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    logging.info(f"단지 {complex_no}의 매물 {len(articles)}개 저장 완료: {file_path}")

def collect_articles_for_complex(complex_info, city, district, dong):
    """특정 단지의 모든 매물 수집"""
    complex_no = complex_info['complexNo']
    deal_count = complex_info['dealCount']
    complex_name = complex_info['complexName']
    
    if deal_count == 0:
        logging.info(f"단지 {complex_name}({complex_no})에는 매물이 없습니다.")
        return
    
    # 페이지 수 계산 (올림)
    total_pages = math.ceil(deal_count / ARTICLES_PER_PAGE)
    logging.info(f"단지 {complex_name}({complex_no}) 매물 수집 시작: 총 {deal_count}개 ({total_pages} 페이지)")
    
    all_articles = []
    
    for page in range(1, total_pages + 1):
        logging.info(f"단지 {complex_name}({complex_no}) 페이지 {page}/{total_pages} 요청 중...")
        
        result = fetch_articles(complex_no, page)
        
        if result and 'articleList' in result:
            articles = result['articleList']
            all_articles.extend(articles)
            logging.info(f"페이지 {page}: {len(articles)}개 매물 수집됨")
            
            # API 요청 간 지연
            time.sleep(REQUEST_DELAY)
        else:
            logging.warning(f"페이지 {page} 요청 실패 또는 비어 있음")
    
    # 수집된 매물 저장
    if all_articles:
        save_articles(complex_no, all_articles, city, district, dong)
    else:
        logging.warning(f"단지 {complex_name}({complex_no})에서 수집된 매물이 없습니다.")

def process_complex_file(file_path):
    """단일 complex 파일 처리"""
    # 파일 경로에서 지역 정보 추출
    parts = file_path.parts
    city_idx = parts.index('complexes') + 1
    city = parts[city_idx]
    district = parts[city_idx + 1]
    dong = parts[-1].split('_')[0]  # 파일명에서 동 이름 추출
    
    logging.info(f"파일 처리 중: {file_path} ({city} {district} {dong})")
    
    # 파일에서 단지 정보 추출
    complexes = get_complexes_from_file(file_path)
    logging.info(f"{len(complexes)}개 단지 정보 로드됨")
    
    # 각 단지별로 매물 수집
    for complex_info in complexes:
        collect_articles_for_complex(complex_info, city, district, dong)

def main():
    """메인 함수"""
    logging.info("매물 수집 시작")
    
    # 데이터 디렉토리 생성
    ARTICLES_DIR_PATH.mkdir(parents=True, exist_ok=True)
    
    # complex 파일 찾기
    complex_files = find_complex_files()
    logging.info(f"총 {len(complex_files)}개 단지 파일 발견됨")
    
    # 각 파일 처리
    for file_path in complex_files:
        process_complex_file(file_path)
    
    logging.info("매물 수집 완료")

if __name__ == "__main__":
    main() 