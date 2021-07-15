import requests
from bs4 import BeautifulSoup
import pandas

import json
import re
import csv

with open("jtbc.json", encoding="utf-8") as json_file:
    jtbc = json.load(json_file)

URL = jtbc["url"] + jtbc["path"] + "pdate=20210714&scode=10&copyright=&pgi=1"

def get_jtbc_news(url, config):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all("dt", {"class": "title_cr"})

    cleaned_results = []
    not_news = False

    for result in results:
        not_news = False

        result = str(result)
        # remove html tag
        result = re.sub('<.+?>', '', result, 0)
        # remove etc words
        result = re.compile('\[[A-za-z가-힣 ]+\]').sub('', result).replace(',','').strip()

        for exclusive in config["exclusive"]:
            if exclusive in str(result):
                not_news = True
                break

        if not_news:
            continue

        cleaned_results.append(result)
    return cleaned_results


def get_date_list(start, end):
    dt_index = pandas.date_range(start=start, end=end)
    date_list = dt_index.strftime("%Y%m%d").tolist()
    return date_list


date_list = get_date_list("20210615", "20210715")

for category in jtbc["query"]["scode"]:
    for date in date_list:

        URL = "{url}{path}pdate={date}&scode={scode}&copyright=&pgi=1".format(
            url=jtbc["url"],
            path=jtbc["path"],
            date=date,
            scode=jtbc["query"]["scode"][category])
        print(URL)

        cleaned_results = get_jtbc_news(URL, jtbc)

        print(cleaned_results)

        with open('jtbc_1.csv', 'a', encoding='utf-8') as f:
            wr = csv.writer(f)

            for result in cleaned_results:
                wr.writerow([result, date, category])

# print(cleaned_results)
