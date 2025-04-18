from datetime import datetime, timedelta


# 수집할 키워드 리스트 (크롤링 엔진 독립적으로 구동 시)
KEYWORDS = ["반도체", "AI"]

# 수집 기준 날짜 (크롤링 엔진 독립적으로 구동 시)
END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(days=1)

# User-Agent 헤더
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
)

# 수집 대상 언론사
TARGET_PRESS_LIST = [
    "연합뉴스", "중앙일보", "조선일보", "동아일보", "한겨레", "경향신문",
    "KBS", "MBC", "SBS", "YTN", "한국경제", "매일경제", "머니투데이"
]



