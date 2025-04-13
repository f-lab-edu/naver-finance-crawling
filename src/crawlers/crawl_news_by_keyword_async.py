import time
from bs4 import BeautifulSoup
from src.crawlers.selenium_driver import get_selenium_driver
from src.crawlers.scroller import infinite_scroll
from src.crawlers.naver_url_builder import set_search_url
from src.crawlers.detail_fetcher import article_detail
from src.utils.common import format_date


async def crawl_news(keyword, start_date, end_date):
    print(f"[INFO] '{keyword}' 뉴스 수집을 시작합니다.")

    search_url = set_search_url(keyword, format_date(start_date), format_date(end_date))
    driver = get_selenium_driver()
    driver.get(search_url)
    time.sleep(1.5)
    infinite_scroll(driver=driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    list_area = soup.find("ul", class_="list_news")

    driver.quit()

    if not list_area:
        print("[WARN] 뉴스 리스트를 찾지 못했습니다.")
        return []

    news_items = list_area.find_all("li", class_="bx")
    print(f"[INFO] 총 {len(news_items)}개의 기사를 찾았습니다.")

    article_basic_info = []
    link_set = set()

    for item in news_items:
        title_tag = item.find("a", class_="news_tit")
        if not title_tag:
            continue

        article_link = title_tag["href"]
        article_title = title_tag["title"]

        if article_link in link_set:
            continue

        link_set.add(article_link)

        press_tag = item.find("a", class_="info press")
        press_name = press_tag.get_text(strip=True) if press_tag else "언론사 알 수 없음"

        article_basic_info.append({
            "title": article_title,
            "link": article_link,
            "press": press_name
        })

        print(article_basic_info)

    return await article_detail(article_basic_info)

