import os
import json
import requests
import time
from bs4 import BeautifulSoup as bs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "woorangzo.settings")

import django

django.setup()
from news.models import Article, Issue

now = time.strftime('%Y-%m-%d')
base_url = 'https://n.news.naver.com/article/'


def crawl_issue():
    result = []
    try:
        resp = requests.get('https://api.thinkpool.com/chart/issue/bubble')
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error : ", e)
    else:
        issue_list = json.loads(resp.text).get('list')

        for issue in issue_list:
            issue['date'] = now
            del issue['issn'], issue['avgRatio']
            result.append(issue['id'])
            Issue(issue_date=issue['date'], issue_keyword=issue['id'], issue_size=issue['size'],
                  issue_groupid=issue['groupid']).save()
    return result


# def crawled_new(data):

def crawl_issue_url(keywords):
    result = {}
    for keyword in keywords:
        print(keyword)
        url_list = []
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sort=1&office_category=3'
        resp = requests.get(url)
        time.sleep(1)
        print(resp.status_code)
        if (resp.status_code == 200) & resp.ok:
            soup = bs(resp.text, 'lxml')
            issue_news_list = soup.find_all('div', class_='info_group')

            for issue_news in issue_news_list:
                if len(issue_news.select('a')) == 2:
                    href = issue_news.select('a')[1]['href']
                    url_list.append(href)

        result[keyword] = url_list

    return result


def crawl_main_url():
    url_list = []
    main_news_url = 'https://m.stock.naver.com/front-api/v1/news/category?category=mainnews&pageSize=50&page=1'

    resp_1 = requests.get(main_news_url)
    if (resp_1.status_code == 200) & resp_1.ok:
        main_news_list = json.loads(resp_1.text)['result']

        for main_news in main_news_list:
            url = main_news['officeId'] + "/" + main_news['articleId']
            news_url = base_url + url
            url_list.append(news_url)

    result = {'main': url_list}
    return result


def crawl_flash_url():
    url_list = []
    flash_news_url = 'https://m.stock.naver.com/front-api/v1/news/category?category=flashnews&pageSize=50&page=1'

    resp_2 = requests.get(flash_news_url)
    if (resp_2.status_code == 200) & resp_2.ok:
        flash_news_list = json.loads(resp_2.text)['result']

        for flash_news in flash_news_list:
            url = flash_news['officeId'] + "/" + flash_news['articleId']
            news_url = base_url + url
            url_list.append(news_url)

    result = {'flash': url_list}
    return result


def crawl_news_detail(result):
    for key, val in result.items():
        news_type = key
        news_url_list = val

        for news_url in news_url_list:

            resp = requests.get(news_url)  # 요청

            if (resp.status_code == 200) & resp.ok:
                soup = bs(resp.text, 'lxml')

                ct = soup.find('div', id='ct')  # content 부분
                office = ct.select_one('img.media_end_head_top_logo_img').attrs['title']  # office 언론사 이름
                title = ct.find('h2', id='title_area').get_text()  # news_title 뉴스 제목
                time = ct.find('span', class_='_ARTICLE_DATE_TIME')['data-date-time']  # 뉴스 입력 시간
                try:
                    writer = ct.find('span', class_='byline_s').get_text()  # 작성자
                except:
                    writer = ''  # 작성자

                article = ct.find('article', id='dic_area')  # 기사 내용 article.text

                if bool(article.find('b')):
                    article.find('b').decompose()
                    # print(article)
                if bool(article.find('span', class_='end_photo_org')):
                    article.find('span', class_='end_photo_org').decompose()

                if bool(article.find('strong')):
                    article.find('strong').decompose()

                content = article.get_text().strip()

                Article(news_office=office, news_title=title, news_time=time, news_writer=writer, news_content=content,
                        news_url=news_url, news_type=news_type).save()

    return print("다 했다!")


# def add_crawled_news():


if __name__ == '__main__':
    start = time.time()  # 테스트용 수정 예정
    # pk나 not null 조건에서는 vaildation check 필요함.
    # PK 수정
    a = crawl_issue()
    b = crawl_issue_url(a)
    c = crawl_main_url()
    d = crawl_flash_url()
    crawl_news_detail(b)
    crawl_news_detail(c)
    crawl_news_detail(d)

    print("time :", time.time() - start)
