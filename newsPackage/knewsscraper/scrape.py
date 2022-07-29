import requests
from bs4 import BeautifulSoup
import json
from time import time
import pandas as pd

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

# utils.py part
TYPE_CONFIG = {
    "사회": "society",
    "정치": "politics",
    "경제": "economic",
    "국제": "foreign",
    "문화": "culture",
    "연예": "entertain",
    "스포츠": "sports",
    "IT": "digital",
    "칼럼": "editorial",
    "보도자료": "press",
}

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def has_next_btn(html, request_type) -> bool:
    if request_type == "search":
        return True
    elif request_type == "normal":
        next_btn = html.select(
            "div.box_etc > div.paging_news > span.inner_paging > a.btn_page.btn_next"
        )
        if len(next_btn) == 0:
            return False
        else:
            return True


def return_select_func(html, request_type) -> list:
    if request_type == "search":
        return html.select("div.cont_divider > ul.list_news > li div.wrap_cont > a")
    elif request_type == "normal":
        return html.select(
            "div.box_etc > ul.list_news2.list_allnews > li div.cont_thumb > strong.tit_thumb > a"
        )


def extract_title(url, params, request_type):
    try:
        original_html = requests.get(url, params=params)
        html = BeautifulSoup(original_html.text, "html.parser")
        title_list = return_select_func(html, request_type)
        if len(title_list) == 0 or not has_next_btn(html, request_type):
            return False
        else:
            return [title.get_text() for title in title_list]
    except Exception as error:
        print("Error from extract_title & error message : ", error)
        return False


def newsType(**kwargs) -> pd.DataFrame:
    THREAD_COUNT = 10
    page_num = 1
    news_title = []

    BASE_URL = "https://news.daum.net/breakingnews/"
    if "newsType" in kwargs:
        URL = f"{BASE_URL}{TYPE_CONFIG[newsType]}"

    if "date" in kwargs:
        URL = f"{BASE_URL}?regDate={date}"

    with ThreadPoolExecutor(THREAD_COUNT) as executor:
        while True:
            url = f"{URL}&page={str(page_num)}"
            future = executor.submit(extract_title, url, "normal")
            page_num = page_num + 1
            break
            if not future.result():
                break

        columns = ["제목"]
        df = pd.DataFrame(news_title, columns=columns)


def set_params(**kwargs) -> dict:
    params_dict = {}
    if "query" in kwargs:
        params_dict.update({"q": kwargs["query"]})

        if "period" in kwargs:
            params_dict.update({"period": kwargs["period"]})

            if kwargs["period"] == "u":
                if "start_date" not in kwargs or "end_date" not in kwargs:
                    print("Error Occurs!")

                else:
                    params_dict.update(
                        {
                            "sd": kwargs["start_date"] + "000000",
                            "ed": kwargs["end_date"] + "235959",
                        }
                    )

        if "article_type" in kwargs:
            params_dict.update({"article_type": kwargs["article_type"]})
        return params_dict

    else:
        print("Error Error")


def newsScrape(**kwargs) -> pd.DataFrame:
    params = set_params(**kwargs)
    THREAD_COUNT = 10
    page_num = 1
    news_title = []
    URL = "https://search.daum.net/search?w=news&DA=STC&enc=utf8"

    with ThreadPoolExecutor(THREAD_COUNT) as executor:
        while page_num < 81:
            params.update({"page": str(page_num)})
            future = executor.submit(extract_title, URL, params, "search")
            page_num = page_num + 1
            if not future.result():
                break
            else:
                news_title = news_title + future.result()
            break
    columns = ["제목"]
    df = pd.DataFrame(news_title, columns=columns)
    return df


if __name__ == "__main__":
    start = time()
    # df = newsType(newsType="경제", date = "20220720")  #newsType="", date=""
    df = newsScrape(query="지구오락실")  # query = "", period="", start_date="", end_date=""
    print(df)
    print("time : ", time() - start)

# [TODO] TYPE_CONFIG에 들어있지 않는 타입 들어왔을때 에러 핸들링
# [TODO] 올바른 date가 아닐때 에러 핸들링
