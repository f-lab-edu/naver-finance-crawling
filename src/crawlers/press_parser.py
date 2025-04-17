from bs4 import BeautifulSoup
from datetime import datetime

from src.utils.common import clean_datetime_string


def parse_article_content(html, press_name):
    """
    각, 언론사별로 기사 본문과 작성일을 추출하는 메서드
    :param html:
    :param press_name:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")
    try:
        if "연합뉴스" in press_name:
            body = soup.find(id="articleWrap")
            published = soup.find("span", class_="txt01")
        elif "중앙일보" in press_name:
            body = soup.find("div", class_="article_body")
            published = soup.find("p", class_="date")
            published = published.find("time")
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
            p_tag = soup.find("div", class_="date").find("p")
            if "입력" in p_tag.get_text(strip=True):
                published = p_tag
        elif "MBC" in press_name:
            body = soup.find("div", class_="news_txt")
            div_tag = soup.find("div", class_="date")
            published = div_tag.find("span")
        elif "YTN" in press_name:
            body = soup.find("div", id="CmAdContent")
            published = soup.find("div", class_="date")
        elif "KBS" in press_name:
            body = soup.find("div", id="cont_newstext")
            published = soup.find("em", class_="input-date")
        elif "SBS" in press_name:
            body = soup.find("div", class_="main_text").find("div", class_="text_area")
            date_area = soup.find("div", class_="date_area")
            published = date_area.find("span")
        elif "한국경제" in press_name:
            body = soup.find("div", id="articletxt")
            published = soup.find("div", class_="datetime").find("span")
        elif "매일경제" in press_name:
            body = soup.find("div", class_="news_cnt_detail_wrap")
            published = soup.find("dl", class_="registration").find("dd")
        elif "머니투데이" in press_name:
            body = soup.find("div", class_="view_text").find("div", id="textBody")
            published = soup.find("li", class_="date").find("time")

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
        for word in ["입력", "작성", "수정"]:
            date_str = date_str.replace(word, "")
        date_str = clean_datetime_string(date_str)
        if "오전" in date_str or "오후" in date_str:
            date_str = date_str.replace("오전", "AM").replace("오후", "PM")
            date = datetime.strptime(date_str, "%Y%m%d %p %I:%M")
        else:
            date = datetime.strptime(date_str[:13], "%Y%m%d %H:%M")
        return date
    except ValueError as e:
        print(f"[Error] 날짜 파싱 실패 ({date_str} - {e})")
        return None

