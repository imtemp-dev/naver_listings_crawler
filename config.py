# API 요청에 필요한 쿠키와 헤더 설정
COOKIES = {
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.trade_type_cd': '""',
    'nhn.realestate.article.ipaddress_city': '1100000000',
    '_fwb': '100qf7Ku8jYuJoQp1DfWC11.1748156567605',
    'landHomeFlashUseYn': 'Y',
    'NAC': 'ye5ZCQhhcHM5B',
    'NACT': '1',
    'NNB': 'KP2D35MZYAZGQ',
    'SRT30': '1748156569',
    'realestate.beta.lastclick.cortar': '1168000000',
    '_fwb': '100qf7Ku8jYuJoQp1DfWC11.1748156567605',
    'SRT5': '1748158034',
    'REALESTATE': 'Sun%20May%2025%202025%2016%3A27%3A28%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'BUC': 'doNQzkKdHTIGC1OAxPGjtq1ai-5BEez_O4jPb1EsMKk=',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NDgxNTgwNDgsImV4cCI6MTc0ODE2ODg0OH0.mAKEQyrYA4mP_XLevKV9QG4VQM4zIVRAIUmemWusgCo',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/search?ms=37.490778,127.0247365,17&a=APT:ABYG:JGC:PRE&e=RETAIL',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}

# 매물 데이터를 저장할 디렉토리
ARTICLES_DIR = "data/articles"
# 한 페이지당 매물 수 (API 응답 기준)
ARTICLES_PER_PAGE = 20
# API 요청 간 지연 시간(초)
REQUEST_DELAY = 1
# 로그 파일 경로
LOG_FILE = "crawler.log"

# API 요청 URL 및 파라미터
BASE_URL = 'https://new.land.naver.com/api/articles/complex'
DEFAULT_PARAMS = {
    'realEstateType': 'APT%3AABYG%3AJGC%3APRE',
    'tradeType': '',
    'tag': '%3A%3A%3A%3A%3A%3A%3A%3A',
    'rentPriceMin': '0',
    'rentPriceMax': '900000000',
    'priceMin': '0',
    'priceMax': '900000000',
    'areaMin': '0',
    'areaMax': '900000000',
    'showArticle': 'false',
    'sameAddressGroup': 'false',
    'priceType': 'RETAIL',
    'type': 'list',
    'order': 'rank'
} 