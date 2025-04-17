import sys
import time
from bs4 import BeautifulSoup
from src.crawlers.selenium_driver import get_selenium_driver
from src.crawlers.scroller import infinite_scroll
from src.crawlers.naver_url_builder import set_search_url
from src.crawlers.detail_fetcher import article_detail
from src.database.database import SessionLocal
from src.database.crud.naver_news_crud import save_articles_bulk
from src.utils.common import format_date


async def crawl_news(keyword, start_date, end_date):
    print(f"[INFO] '{keyword}' 뉴스 수집을 시작합니다.")

    # search_url = set_search_url(keyword, format_date(start_date), format_date(end_date))
    search_url_test = "https://search.naver.com/search.naver?ssc=tab.news.all&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E" \
                      "%90&sm=tab_opt&sort=0&photo=0&field=0&pd=12&ds=&de=&docid=&related=0&mynews=0&office_type=0" \
                      "&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0" \
                      "&office_category=&service_area= "
    driver = get_selenium_driver()
    # driver.get(search_url)
    driver.get(search_url_test)
    time.sleep(1.5)
    infinite_scroll(driver=driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    list_area = soup.find("ul", class_="list_news")

    driver.quit()

    if not list_area:
        print("[WARN] 뉴스 리스트를 찾지 못했습니다.")
        return []

    news_items = list_area.find_all("div", class_="sds-comps-vertical-layout sds-comps-full-layout "
                                                  "Ermefm6A3ilpd9Zvt0OZ")
    print(f"[INFO] 총 {len(news_items)}개의 기사를 찾았습니다.")

    article_basic_info = []
    link_set = set()
    for item in news_items:
        title_tag = item.find("a", class_="bynlPWBHumGsbotLYK9A jT1DuARpwIlNAFMacxlu")
        if not title_tag:
            continue
        article_link = title_tag["href"]
        article_title = title_tag.find("span").get_text(strip=True).strip()

        if article_link in link_set:
            continue

        link_set.add(article_link)

        press_tag = item.find("span", class_="sds-comps-text sds-comps-text-type-body2 sds-comps-text-weight-sm")
        press_name = press_tag.get_text(strip=True).strip() if press_tag else "언론사 알 수 없음"

        article_basic_info.append({
            "title": article_title,
            "link": article_link,
            "press": press_name
        })

    # 기사 상세 정보를 비동기 수집
    articles = await article_detail(article_basic_info)
    print(articles)

    # 수집된 기사 정보 DB에 한번에 삽입
    db_session = SessionLocal()
    save_articles_bulk(db_session, articles)
    db_session.close()

    return articles


