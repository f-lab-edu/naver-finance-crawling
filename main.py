import json
import time

from src.crawlers.naver_finance_crawler import NaverFinanceCrawler


def main():
    # 작업 시간 측정을 위해
    start_time = time.time()
    crawler = NaverFinanceCrawler()
    links = crawler.collect_news_links()
    print(f"총 {len(links)}개의 링크를 수집했습니다.")

    articles = crawler.crawl_articles(links)
    print(f"총 {len(json.loads(articles)['news'])}개의 기사를 수집했습니다.")
    print(articles)

    end_time = time.time()

    total_crawl_time = end_time - start_time
    print(f"수집이 완료되었습니다. 총 작업시간: {total_crawl_time:.2f}초")

if __name__ == "__main__":
    main()
