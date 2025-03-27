import json
from datetime import datetime
from typing import Dict
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

from src.crawlers.crawler import Crawler


class NaverFinanceCrawler(Crawler):
    """
    네이버 금융 뉴스 기사 링크와 링크의 기사내용을 수집하는 클래스 (Crawler 상속)
    """
    BASE_URL: str = "https://finance.naver.com/news/news_list.naver?"
    NEWS_TABS: Dict[str, Dict[str, str]] = {
        "realtime": {
            "query": "mode=LSS2D&section_id=101&section_id2=258&page=",
            "tag": "dd",
            "selector": "articleSubject"
        },
        "most_view": {
            "query": "mode=RANK&page=",
            "tag": "ul",
            "selector": "simpleNewsList"
        }
    }

    def extract_article_link(self, article_url):
        """
        네이버 금융 기사 URL을 네이버 뉴스 URL로 변환하는 함수
        :param article_url:
        :return:
        """
        try:
            parsed_url = urlparse(article_url)
            query_param = parse_qs(parsed_url.query)
            office_id = query_param.get("office_id", [None])[0]  # office id
            article_id = query_param.get("article_id", [None])[0]  # article id

            # office id 와 article id 모두 존재하는 경우에만 뉴스 URL 반환
            if office_id and article_id:
                return f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"

        except Exception as e:
            print(f"URL 파싱 오류 발생 url: {article_url} - error: {e}")

        return None

    def fetch_all_pages(self, query: str, tag: str, selector: str):
        """
        해당 탭의 모든 페이지에서 뉴스 기사 링크를 수집하는 함수 (예: 페이지 1 ~ 10까지 리스팅된 기사의 링크)
        :param query:
        :param tag:
        :param selector:
        :return:
        """
        page: int = 1  # 시작 페이지 번호
        collected_links = set()  # 수집될 링크 - 중복방지를 위해 set()을 사용
        previous_links = set()  # 이전 페이지의 수집된 링크 - 무한 루프 방지를 위해 사용

        # 수집 할 페이지가 있을 동안 루프
        while True:
            url: str = f"{self.BASE_URL}{query}{page}"  # 베이스URL + URL query + 페이지 번호
            html = self.fetch_html(url)
            if not html:
                break  # 더 이상 수집할 HTML이 없다면 루프 종료

            news_items = self.parse_html(html, tag, selector)  # 수집된 HTML을 Beautifulsoup 객체로 변환
            article_links = set()
            for item in news_items:
                link_tag = item.find("a")  # 기사 링크를 획득하기 위한 a태그 탐색
                if link_tag and link_tag.get("href"):
                    article_link = self.extract_article_link(link_tag.get("href"))
                    if article_link:
                        article_links.add(article_link)
            print(article_links)

            if not article_links or article_links == previous_links:
                print(f"{page}페이지에서 새로 수집 할 기사 링크 없음 루프 종료")
                break

            collected_links.update(article_links)
            previous_links = article_links
            page += 1  # 중단 없이 모든 과정 진행되었다면 페이지 증가

        return list(collected_links)  # 수집된 기사 링크 반환

    def collect_news_links(self):
        all_article_links = set()

        for tab, info in self.NEWS_TABS.items():
            print(f"탭 {tab} 링크 수집을 시작합니다...")
            article_links = self.fetch_all_pages(info['query'], info['tag'], info['selector'])
            all_article_links.update(article_links)

        return list(all_article_links)

    def crawl_articles(self, article_links):
        """
        수집된 기사 링크에서 기사 본문을 크롤링하는 함수
        :param article_links:
        :return:
        """

        articles = {"news": []}  # 기사 제목, 본문, 작성일 을 담을 변수

        for link in article_links:

            print(f"기사 크롤링을 시작합니다. link: {link}")
            html = self.fetch_html(link)
            if not html:
                continue  # 크롤링 할 기사가 더 이상 없다면 건너뛰기

            soup = BeautifulSoup(html, "html.parser")
            article_title_tag = soup.find("h2", id="title_area")
            article_content_tag = soup.find("article", id="dic_area")
            article_publish_tag = soup.find("span", class_="media_end_head_info_datestamp_time")

            article_title = article_title_tag.get_text(strip=True) if article_title_tag else None
            article_content = article_content_tag.get_text(strip=True) if article_content_tag else None
            article_publish_date = article_publish_tag.get("data-date-time") if article_publish_tag else None

            # print(f"제목: {article_title}, 본문: {article_content}, 등록일: {article_publish_date}")

            articles["news"].append(
                {
                    "title": article_title,
                    "content": article_content,
                    "publish_date": article_publish_date
                }
            )

        return json.dumps(articles, ensure_ascii=False, indent=4)






