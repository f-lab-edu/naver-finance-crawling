from bs4 import BeautifulSoup
from datetime import datetime


def parse_article_content(html, press_name):
    """
    각, 언론사별로 기사 본문과 작성일을 추출하는 메서드
    :param html:
    :param press_name:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")

    body, published_date = None, None

    try:
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
            body = soup.find("section", class_="news_view")
            date_div = soup.find("div", id="dateInfo")
            published = date_div.find("p").find("span") if date_div else None
        elif "한겨레" in press_name:
            body = soup.find("div", class_="text")
            ul_tag = soup.find("ul", class_="ArticleDetailView_dateList__tniXJ")
            if ul_tag:
                for li in ul_tag.find_all("li"):
                    if "등록" in li.text:
                        published = li.find("span")
        elif "경향신문" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("div", class_="date").find("p")
        elif press_name in ["KBS", "MBC", "YTN"]:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date")
        elif "SBS" in press_name:
            body = soup.find("div", class_="text")
            published = soup.find("span", class_="date-published")
        elif "한국경제" in press_name:
            body = soup.find("div", class_="article-body-wrap")
            published = soup.find("span", class_="txt-date")
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
        published_date = _parse_date(published.get_text(strip=True)) if published else ""

        return {
            "content": content,
            "pub_date": published_date
        }
    except Exception as e:
        print(f"[Error] 파싱 실패 ({press_name}) - {e}")
        return None


def _parse_date(date_str):
    """
    추출된 작성일 텍스트를 datetime 객체로 변환 처리 하는 메서드
    :param date_str:
    :return:
    """
    try:
        if "입력" in date_str:
            date_str = date_str.replace("입력", "").strip()
        elif "작성" in date_str:
            date_str = date_str.replace("작성", "").strip()

        return datetime.strptime(date_str[:16], "%Y.%m.%d %H:%M")
    except ValueError as e:
        print(f"[Error] 날짜 파싱 실패 ({date_str})")
        return None
