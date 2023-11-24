from bs4 import BeautifulSoup as bs
import requests, json, time

now = time.strftime('%Y-%m-%d')
base_url = 'https://n.news.naver.com/article/'


def crawl_issue():
    """
    :return: 당일 이슈 데이터/ 차트 그릴 때 필요함
    """

    result = []  # 결과 담아 주기 위한 리스트 생성

    try:
        # requests 라이브러리 사용하여 get 방식으로 호출
        resp = requests.get('https://api.thinkpool.com/chart/issue/bubble')

        resp.raise_for_status()  # 응답 확인 > 안되면 error

    except requests.exceptions.RequestException as e:
        # try ~ except문으로 오류 처리 , 뭐 나올지 몰라서 RequestException으로 함
        print("Error : ", e)
    else:
        # json 패키지 loads()로 딕셔너리로 만듬 , list 부분만 사용
        issue_list = json.loads(resp.text).get('list')

        for issue in issue_list:
            issue['date'] = now  # 당일 날짜 추가
            del issue['issn'], issue['avgRatio']  # for 문 돌려서 필요 없는 데이터 삭제
            result.append(issue)  # result 리스트에 담아서 리턴

    return result


# def crawled_new(data):

def crawl_news_url(keywords):
    """
    :param keywords: crawl_issue()의 return 값에서 'id'값만 가져 온다.
    :return: 네이버 뉴스 상세페이지 주소 리스트를 리턴한다.
    """

    result = []
    # for issue in issue_list:
    #     keywords.append(issue['id'])  # id만 추출해서 리스트에 담음

    for keyword in keywords:
        # 검색어로 뉴스 리스트 페이지 크롤링
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sort=1&office_category=3'
        resp = requests.get(url)

        if (resp.status_code == 200) & resp.ok:  # 연결 확인
            soup = bs(resp.text, 'lxml')  # beatifulsoup 객체 생성
            naver_new_list = soup.find_all('div', class_='info_group')  # 파싱

            for naver_new in naver_new_list:  # 리스트에서 for 문으로 url만 출력
                if len(naver_new.select('a')) == 2:
                    a = naver_new.select('a')[1]['href']
                    result.append(a)

    main_news_url = 'https://m.stock.naver.com/front-api/v1/news/category?category=mainnews&pageSize=50&page=1'

    resp_1 = requests.get(main_news_url)
    if (resp_1.status_code == 200) & resp_1.ok:
        main_news_list = json.loads(resp_1.text)['result']

        for main_news in main_news_list:
            url = main_news['officeId'] + "/" + main_news['articleId']
            news_url = base_url + url
            result.append(news_url)

    flash_news_url = 'https://m.stock.naver.com/front-api/v1/news/category?category=flashnews&pageSize=50&page=1'

    resp_2 = requests.get(flash_news_url)
    if (resp_2.status_code == 200) & resp_2.ok:
        flash_news_list = json.loads(resp_2.text)['result']

        for flash_news in flash_news_list:
            url = flash_news['officeId'] + "/" + flash_news['articleId']
            news_url = base_url + url
            result.append(news_url)

    return result


def crawl_news_detail(url):
    """
    :param officeid: 언론사 아이디
    :param articleid: 기사 아이디
    :return: DB에 뉴스 데이터 넣어줌
    """

    # 샘플 상세페이지 > 네이버 뉴스 상세페잉지

    resp = requests.get(url)  # 요청

    if (resp.status_code == 200) & resp.ok:
        soup = bs(resp.text, 'lxml')

        ct = soup.find('div', id='ct')  # content 부분
        news_office = ct.select_one('img.media_end_head_top_logo_img').attrs['title']  # office 언론사 이름
        news_title = ct.find('h2', id='title_area').get_text()  # news_title 뉴스 제목
        news_time = ct.find('span', class_='_ARTICLE_DATE_TIME')['data-date-time']  # 뉴스 입력 시간
        try:
            news_writer = ct.find('span', class_='byline_s').get_text()  # 작성자
        except:
            news_writer = ''  # 작성자

        news_article = ct.find('article', id='dic_area')  # 기사 내용 article.text

        if bool(news_article.find('b')):
            news_article.find('b').decompose()
            # print(article)
        if bool(news_article.find('span', class_='end_photo_org')):
            news_article.find('span', class_='end_photo_org').decompose()

        if bool(news_article.find('strong')):
            news_article.find('strong').decompose()

        news_content = news_article.get_text().strip()

        return news_office, news_title, news_time, news_writer, news_content  # 수정 예정


if __name__ == '__main__':
    start = time.time() # 테스트용 수정 예정
    # issue = crawl_issue()
    # print(issue)
    # url_list = crawl_news_url(issue)
    # print(url_list)
    # for url in url_list:
    #     detail = crawl_news_detail(url)
    #     print(detail)
    print("time :", time.time() - start)
