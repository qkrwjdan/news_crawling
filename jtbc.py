import requests
from bs4 import BeautifulSoup

import json
import re

with open("jtbc.json", encoding="utf-8") as json_file:
    jtbc = json.load(json_file)

def get_jtbc_news(url, config):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all("dt", {"class": "title_cr"})
    print(results)

    cleaned_results = []
    not_news = False

    for result in results:
        not_news = False

        result = str(result)
        result = re.sub('<.+?>', '', result, 0).strip()
        print(result)
        for exclusive in config["exclusive"]:
            if exclusive in str(result):
                not_news = True
                break

        if not_news:
            continue

        cleaned_results.append(result)
    return cleaned_results

URL = jtbc["url"] + jtbc["path"] + "pdate=20210714&scode=10&copyright=&pgi=1"

cleaned_results = get_jtbc_news(URL,jtbc)
print(cleaned_results)
