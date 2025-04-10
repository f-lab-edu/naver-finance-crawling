import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from src.crawlers.crawl_news_by_keyword import crawl_news

st.set_page_config(page_title="네이버 뉴스 크롤러", layout="wide")

st.title("실시간 네이버 뉴스 크롤러")
st.markdown("네이버 뉴스에서 검색 키워드에 따른 주요 언론사의 기사를 수집합니다.")

# 사이드 바: 수집 설정 값 입력
st.sidebar.header("뉴스 수집 설정")

keywords = st.sidebar.text_input("수집 키워드 (쉼표 구분)", value="삼성전자, 반도체")

date_range = st.sidebar.date_input(
    "수집기간을 선택해 주세요",
    value=(datetime.today() - timedelta(days=1), datetime.today())
)

start_date = datetime.combine(date_range[0], datetime.min.time())
end_date = datetime.combine(date_range[1], datetime.max.time())

if st.sidebar.button("뉴스 수집"):
    with st.spinner("뉴스를 수집 중입니다..."):
        keyword_list = [kw.strip() for kw in keywords.split(",")]

        collect_result = []

        for keyword in keyword_list:
            results = crawl_news(keyword, start_date, end_date)
            collect_result.extend(results)

        print(collect_result)
        dataframe = pd.DataFrame(collect_result)
        st.success(f"총 {len(dataframe)}건의 뉴스가 수집 되었습니다.")
        st.dataframe(dataframe[["title", "press", "pub_date", "content"]])

