from urllib.parse import quote, urlencode


def set_search_url(keyword, start_date, end_date):
    base_url = "https://search.naver.com/search.naver?"

    start_str = start_date.replace(".", "")
    end_str = end_date.replace(".", "")

    query_params = {
        "where": "news",
        "query": keyword,
        "sm": "tab_opt",
        "sort": "1",
        "photo": "0",
        "field": "0",
        "pd": "4",
        "ds": start_date,
        "de": end_date,
        "nso": f"so:dd,p:from{start_str}to{end_str},a:all",
    }

    return f"{base_url}{urlencode(query_params, quote_via=quote)}"
