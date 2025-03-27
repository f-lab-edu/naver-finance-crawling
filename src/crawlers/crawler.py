import time

import requests
from bs4 import ResultSet, BeautifulSoup
from requests import Response


class Crawler:
    """
    크롤링 기본 클래스
    """
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/134.0.0.0 Safari/537.36"
    }

    @staticmethod
    def fetch_html(url: str):
        """
        주어진 URL에서 HTML을 가져오는 함수

        :param url:
        :return:
        """
        try:
            response: Response = requests.get(url, headers=Crawler.HEADERS)
            response.raise_for_status()
            time.sleep(1.5)
            return response.text
        except requests.RequestException as e:
            print(f"페이지 로드 실패 url: {url} - error: {e}")
            return None  # 예외 발생시 None 반환

    @staticmethod
    def parse_html(html: str, tag: str, selector: str):
        """
        HTML에서 특정 태그와 셀렉터를 가진 요소를 추출

        :param html:
        :param tag:
        :param selector:
        :return:
        """
        soup: ResultSet = BeautifulSoup(html, "html.parser")
        return soup.find_all(tag, class_=selector)
