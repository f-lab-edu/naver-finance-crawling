import time
from datetime import datetime, timedelta
from urllib.parse import quote, urlencode

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Selenium 크롬 옵션 설정


# 수집할 키워드 리스트
KEYWORDS = ["반도체", "AI", "삼성전자"]

# 수집 기준 날짜
END_DATE = datetime.today()
# START_DATE = END_DATE - timedelta(days=90)  # 수집 시작일은 수집일 기준 3개월 이전
START_DATE = END_DATE - timedelta(hours=1)  # 기능 테스트 용도

# 헤더에 추가 할 User-Agent 정보
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "\
             "Chrome/134.0.0.0 Safari/537.36"

TARGET_PRESS_LIST = [
    "연합뉴스", "중앙일보", "조선일보", "동아일보", "한겨레", "경향신문", "KBS", "MBC", "SBS",
    "YTN", "한국경제", "매일경제", "머니투데이", "뉴스1", "뉴시스"
]


def format_date(date):
    """ 날짜 포맷을 YYYY.MM.DD로 변환하여 반환 """
    return date.strftime("%Y.%m.%d")


def get_selenium_driver():
    """ Selenium 웹 드라이버 설정 메서드 """
    options = Options()
    options.add_argument("--headless")  # 브라우저 창 없이
    options.add_argument(f"user-agent={USER_AGENT}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)  # 크롬 드라이버 반환


def set_search_url(keyword, start_date, end_date):
    base_url = "https://search.naver.com/search.naver?"

    nso_range = f"so:dd,p:from{start_date}to{end_date},a:all"

    # nso 파라미터 용도
    start_str = start_date.replace(".", "")
    end_str = end_date.replace(".", "")

    query_params = {
        "where": "news",  # 검색 대상: 뉴스
        "query": keyword,  # 검색어 - 예) 삼성전자
        "sm": "tab_opt",  # 검색 방식 구분자
        "sort": "1",  # 정렬 방식: 0 = 정확도순, 1 = 최신순
        "photo": "0",  # 이미지 포함 필터: 0 = 전체, 1 = 포함된 기사만
        "field": "0",  # 검색 범위: 0 = 전체, 1 = 제목만
        "pd": "4",  # 날짜 범위: 0 = 전체, 1 = 1일, 2 = 1주, 3 = 1개월, 4 = 사용자 지정
        "ds": start_date,  # 검색 시작 날짜 및 시간
        "de": end_date,  # 검색 종료 날짜 및 시간
        # "docid": "",  # 특정 문서 ID 필터 (공백)
        # "mynews": "0",  # 내 구독 언론사만 보기: 0=전체, 1=사용
        # "office_type": "0",  # 언론사 분류: 0=전체, 1=인터넷, 2=지면
        # "office_section_code": "0",  # 언론사 섹션 코드
        # "news_office_checked": "",  # 선택된 언론사 코드들 (, 구분)
        # "nso": f"so:dd,p:from{start_date}to{end_date},a:all",  # 날짜 범위 정렬 조건 (from ~ to 범위 포함)
        "nso": f"so:dd,p:from{start_str}to{end_str},a:all",  # 날짜 범위 정렬 조건 (from ~ to 범위 포함)
        # "is_sug_officeid": "0",  # 제안된 언론사 필터 사용 여부
        # "office_category": "0",  # 언론사 분류 필터: 0=전체
        # "service_area": "0"  # 서비스 영역
    }
    return f"{base_url}{urlencode(query_params, quote_via=quote)}"


def infinite_scroll(driver, wait_time=1, max=100):
    scroll_count = 0
    while scroll_count < max:
        prev_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(wait_time)
        cur_height = driver.execute_script("return document.body.scrollHeight")
        if prev_height == cur_height:
            break

        scroll_count += 1


# Selenium 사용
# def get_article_detail_(url, press_name, driver):
#
#     target_press_list = [
#         "연합뉴스", "중앙일보", "조선일보", "동아일보", "한겨레", "경향신문", "KBS", "MBC", "SBS",
#         "YTN", "한국경제", "매일경제", "머니투데이", "뉴스1", "뉴시스"
#     ]
#
#     if not any(name in press_name for name in target_press_list):
#         print(f"[스킵] 수집 대상 언론사가 아닙니다: {press_name}")
#         return None, None
#
#     try:
#         # 현재 탭 저장
#         origin_tab = driver.current_window_handle
#
#         # 새 탭을 열고 해당 기사 링크로 이동
#         driver.execute_script("window.open(arguments[0]);", url)
#         driver.switch_to.window(driver.window_handles[-1])
#         time.sleep(1.5)
#
#         soup = BeautifulSoup(driver.page_source, "html.parser")
#
#         if "연합뉴스" in press_name:
#             body = soup.find(id="articleWrap")
#             published = soup.find("span", class_="update-time")
#         elif "중앙일보" in press_name:
#             body = soup.find("div", class_="article_body")
#             published = soup.find("p", class_="byline")
#         elif "조선일보" in press_name:
#             body = soup.find("div", id="news_body_id")
#             published = soup.find("span", class_="date")
#         elif "동아일보" in press_name:
#             body = soup.find("div", class_="article_txt")
#             published = soup.find("span", class_="date01")
#         elif "한겨레" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="date-time")
#         elif "경향신문" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="pubdate")
#         elif "KBS" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="date")
#         elif "MBC" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("div", class_="input-time") or soup.find("span", class_="date")
#         elif "SBS" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="date-published")
#         elif "YTN" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="date")
#         elif "한국경제" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="date-time")
#         elif "매일경제" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="lasttime")
#         elif "머니투데이" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="date")
#         elif "뉴스1" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="article_date")
#         elif "뉴시스" in press_name:
#             body = soup.find("div", class_="text")
#             published = soup.find("span", class_="date")
#
#         driver.close()
#         driver.switch_to.window(origin_tab)
#
#         content = body.get_text(strip=True) if body else ""
#         if published:
#             date_str = published.get_text(strip=True)
#             try:
#                 published_date = datetime.strptime(date_str[:16], "%Y.%m.%d %H:%M")
#             except ValueError:
#                 print(f"날짜 형식 파싱 실패: {date_str}")
#                 published_date = None
#         else:
#             published_date = None
#
#         return content, published_date
#     except Exception as e:
#         print(f"본문 수집 중 에러 발생 [{press_name}] - {e}")
#         driver.close()
#         driver.switch_to.window(origin_tab)


# requests 사용
def get_article_detail(url, press_name):
    if not any(name in press_name for name in TARGET_PRESS_LIST):
        print(f"[스킵] 수집 대상 언론사가 아닙니다: {press_name}")
        return None, None

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        if response.status_code != 200:
            print(f"[error] 수집 요청 실패 ({response.status_code}) - {url}")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")

        if "연합뉴스" in press_name:
            body = soup.find(id="articleWrap")
            published = soup.find("span", class_="txt01")
        elif "중앙일보" in press_name:
            body = soup.find("div", class_="article_body")
            published = soup.find("p", class_="date")
        elif "조선일보" in press_name:
            body = soup.find("div", id="news_body_id")
            published = soup.find("span", class_="inputDate")
        elif "동아일보" in press_name:
            body = soup.find("div", class_="article_txt")
            date_div = soup.find("div", id="dateInfo")
            p_tag = date_div.find("p")
            published = p_tag.find("span")
        elif "한겨레" in press_name:
            body = soup.find("div", class_="text")
            published = None
            ul_tag = soup.find("ul", class_="ArticleDetailView_dateList__tniXJ")
            li_tags = ul_tag.find_all("li")
            for li in li_tags:
                if "등록" in li.text:
                    published = li.find("span")
        elif "경향신문" in press_name:
            body = soup.find("div", class_="text")
            date_div = soup.find("div", class_="date")
            published = date_div.find("p")
        elif "KBS" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date")
        elif "MBC" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date")
        elif "SBS" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date-published")
        elif "YTN" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date")
        elif "한국경제" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date-time")
        elif "매일경제" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="lasttime")
        elif "머니투데이" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date")
        elif "뉴스1" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="article_date")
        elif "뉴시스" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date")

        content = body.get_text(strip=True) if body else ""

        if published:
            # 작성일 정보가 존재 할 경우에 텍스트 추출
            date_str = published.get_text(strip=True)
            try:
                # 수집된 텍스트에 입력 혹은 작성 이라는 단어가 포함되어 있다면 제거 후 공백도 제거
                if "입력" in date_str:
                    date_str = date_str.replace("입력", "").strip()
                elif "작성" in date_str:
                    date_str = date_str.replace("작성", "").strip()
                # 추출된 문자열 16자 까지 슬라이싱 후 포맷 변경
                published_date = datetime.strptime(date_str[:16], "%Y.%m.%d %H:%M")
            except ValueError:
                # 포맷이 잘못되어 파싱에 실패할 경우의 예외 처리
                print(f"날짜 형식 파싱 실패: {date_str}")
                published_date = None
        else:
            published_date = None

        return content, published_date
    except Exception as e:
        print(f"본문 수집 중 에러 발생 [{press_name}] - {e}")
        return None, None


def crawl_news(keyword, start_date, end_date):
    print(f"{keyword} 중심으로 뉴스 수집을 시작 합니다....")  # 추후 로그로 변경

    search_url = set_search_url(keyword, format_date(start_date), format_date(end_date))

    web_driver = get_selenium_driver()  # selenium 드라이버
    web_driver.get(search_url)
    time.sleep(2)  # 수집 대상 서버 과부화를 피하기 위한 대기 시간
    infinite_scroll(driver=web_driver)  # 테스트 용도로 기간과 상관없이 스크롤링 10번만 진행

    soup = BeautifulSoup(web_driver.page_source, "html.parser")
    list_area = soup.find("ul", class_="list_news")
    if not list_area:
        print("뉴스 리스트를 찾지 못했습니다.")
        web_driver.quit()
        return []  # 빈 리스트 반환

    news_items = list_area.find_all("li", class_="bx")
    print(f"총 {len(news_items)}개의 기사를 찾았습니다.")

    results = []
    links = set()  # 기사 중복 방지를 위한 링크 집합

    for item in news_items:
        # 기사 상세 링크, 기사 제목 추출
        title_tag = item.find("a", class_="news_tit")
        article_link = title_tag["href"]  # 기사 상세 링크
        article_title = title_tag["title"]  # 기사 제목

        # 링크 중복 제거 (기존에 수집된 링크라면 패스)
        if article_link in links:
            continue

        links.add(article_link)

        # 신문사 추출
        press_tag = item.find("a", class_="info press")
        press_name = press_tag.get_text(strip=True) if press_tag else None

        # 여기서 부터 각, 신문사별 개별 스크래핑 진행... (네이버 뉴스는 네이버 자체 뉴스가 아니기 때문에 본문 수집을 위해선 개별 처리 필요)
        # content, published = get_article_detail(article_link, press_name, web_driver)
        content, published = get_article_detail(article_link, press_name)

        if content:
            results.append({
                "title": article_title,
                "link": article_link,
                "press": press_name,
                "pub_date": published,
                "content": content
            })

    web_driver.quit()
    return results

