import aiohttp
import asyncio
from src.crawlers.press_parser import parse_article_content
from src.crawlers.config import USER_AGENT, TARGET_PRESS_LIST


async def get_article_detail(session, url, press_name):
    if not any(name in press_name for name in TARGET_PRESS_LIST):
        return None

    try:
        async with session.get(url, headers={"User-Agent": USER_AGENT}, timeout=aiohttp.ClientTimeout(total=10)) as res:
            if res.status != 200:
                print(f"[Error] 요청 실패 ({res.status}) - {url}")
                return None

            html = await res.text()
            return parse_article_content(html=html, press_name=press_name)

    except Exception as e:
        print(f"[Error] 기사 본문 수집 실패 ({press_name}) - {e}")
        return None


async def article_detail(article_basic_info):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_article_detail(session=session, url=item["link"], press_name=item["press"])
            for item in article_basic_info
        ]
        fetched = await asyncio.gather(*tasks)

        for index, detail in enumerate(fetched):
            if detail is None:
                continue

            article = article_basic_info[index]
            results.append({
                "title": article["title"],
                "link": article["link"],
                "press": article["press"],
                "pub_date": detail.get("pub_date"),
                "content": detail.get("content")
            })
    print(results)
    return results

# asyncio.run(article_detail([
#     {
#         "title": "한숨 돌린 삼성…폰·메모리 업황 회복 기대",
#         "link": "https://www.hankyung.com/article/2025041383381",
#         "press": "한국경제"
#     },
#     {
#         "title": "스마트폰 상호관세 면제에 한숨 돌린 삼성…반도체는 여전히 긴장",
#         "link": "https://www.donga.com/news/Economy/article/all/20250413/131403066/1",
#         "press": "동아일보"
#     }
# ]))
