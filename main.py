import streamlit as st
import json
import time

from src.crawlers.naver_finance_crawler import NaverFinanceCrawler

if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="네이버 금융 뉴스 수집"
    )
    st.markdown(
        """
        <h2>네이버 금융 뉴스 수집</h2>
        <hr>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("설정")
    url = st.sidebar.text_input("수집 URL", max_chars=300, placeholder="ex) https://abc.com")
    tag = st.sidebar.text_input("HTML 태그입력", max_chars=300, placeholder="ex) a")
    css_selector = st.sidebar.text_input("CSS 선택자 입력", max_chars=300, placeholder="ex) articleSubject")
    collect_button = st.sidebar.button("데이터 수집")

    def collect_data(url: str, tag: str, selector: str):
        if not url:
            st.toast("수집할 페이지 URL을 입력해주세요!", icon="⚠️")
        elif not tag:
            st.toast("대상 HTML 태그를 입력해주세요!", icon="⚠️")
        elif not selector:
            st.toast("대상 CSS 선택자를 입력해주세요!", icon="⚠️")
        else:
            st.write(f"수집을 시작: {url}에서 수집중....")
            


    if collect_button:
        collect_data(url, tag, css_selector)
    # 작업 시간 측정을 위해
    # start_time = time.time()
    # crawler = NaverFinanceCrawler()
    # links = crawler.collect_news_links()
    # print(f"총 {len(links)}개의 링크를 수집했습니다.")
    #
    # articles = crawler.crawl_articles(links)
    # print(f"총 {len(json.loads(articles)['news'])}개의 기사를 수집했습니다.")
    # print(articles)
    #
    # end_time = time.time()
    #
    # total_crawl_time = end_time - start_time
    # print(f"수집이 완료되었습니다. 총 작업시간: {total_crawl_time:.2f}초")
