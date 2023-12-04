import json
import requests
import time
import mysql.connector
from bs4 import BeautifulSoup as bs

mydb = mysql.connector.connect(
    host="localhost",
    user="woorangzo",
    passwd="1234",
    database="woorangzo"
)

mc = mydb.cursor(prepared=True)

now = time.strftime('%Y-%m-%d')
base_url = 'https://n.news.naver.com/article/'


def crawl_issue_keywords():
    """
    ThinkPool 사이트에서 이슈 관련 정보 크롤링 하는 메소드 / 이슈 날짜, 키워드, 사이즈, 그룹 저장
    :return: issue keyword 리스트 형식으로 리턴
    """
    mc.execute("delete from issue")
    mydb.commit()
    data = []
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
            data.append((issue['date'], issue['id'], issue['size'], issue['groupid']))

    sql = 'INSERT INTO issue (issue_date, issue_keyword, issue_size, issue_group) VALUES (?,?,?,?)'
    try:
        mc.executemany(sql, data)
    except mysql.connector.Error as err:
        print("Error:", err)
    mydb.commit()
    keywords = []
    for i in data:
        keywords.append(i[1])

    return keywords


def crawl_issue(keywords):
    """
    crawl_issue()에서 리턴 받은 키워드 뉴스 페이지 크롤링 메소드 / news_id, 언론사, 제목, 내용 일부분, 이슈 키워드, 뉴스 타입 저장
    :param keywords: crawl_issue() 에서 리턴 되는 keyword 리스트
    :return: news_id pk 리스트 형식으로 리턴
    """
    find_all = "select news_id from news"
    try:
        mc.execute(find_all)
    except mysql.connector.Error as err:
        print('main find_all Error : ', err)
    prev_data = mc.fetchall()
    result = []
    for keyword in keywords:
        data = []
        news_num = 1
        while news_num < 20:

            url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sort=1&office_category=3&start={news_num}'
            resp = requests.get(url)
            time.sleep(1)

            soup = bs(resp.text, 'lxml')
            issue_news_list = soup.find_all('div', class_='news_area')

            for issue_news in issue_news_list:
                naver_news = issue_news.find('div', class_='info_group').select('a')
                if len(naver_news) == 2:
                    href = naver_news[1]['href']

                    try:
                        url = href[0:href.index('?')]
                        url_parameter = url.split('/')
                        news_id = url_parameter[5] + url_parameter[6]
                        result.append(news_id)  # pk
                        pick = issue_news.find('i', 'spnew ico_pick')

                        if pick in issue_news.find('a', class_='info press'):
                            pick.decompose()
                        issue_news_office = issue_news.find('a', class_='info press').get_text()  # 언론사
                        issue_news_title = issue_news.find('a', class_='news_tit')['title']  # 뉴스 제목
                        issue_news_content = issue_news.find('a', class_='api_txt_lines dsc_txt_wrap').get_text()[
                                             0:80]  # 뉴스 내용
                        if (news_id,) not in prev_data:
                            data.append((news_id, issue_news_office, issue_news_title, issue_news_content, keyword))
                    except IndexError:
                        pass



            news_num += 10

        sql = "INSERT INTO news (news_id,news_office_nm,news_title,news_content,news_type) VALUES (?,?,?,?,?)"
        try:
            mc.executemany(sql, data)
        except mysql.connector.Error as err:
            print("issue Error:", err)
            pass
        mydb.commit()
    return result


def update_issue():
    """
    이슈 뉴스 업데이트 메소드
    :return: DB에서 키워드 가져와 crawl_issue_news() 실행
    """
    sql = "select issue_keyword  from issue"
    try:
        mc.execute(sql)
    except mysql.connector.Error as err:
        print("issue update Error:", err)
    keywords = mc.fetchall()
    data = []
    for keyword in keywords:
        data.append(keyword[0])
    print(data)
    result = crawl_issue(data)
    return crawl_news_detail(result)


def crawl_main():
    """
    주요 뉴스 크롤링 메소드 / news_id, 언론사, 제목, 내용 일부분, 뉴스 타입 저장
    :return: pk news_id 리스트 형식으로 리턴
    """
    find_all = "select news_id from news"
    try:
        mc.execute(find_all)
    except mysql.connector.Error as err:
        print('main find_all Error : ', err)
    prev_data = mc.fetchall()
    data = []
    result = []
    main_news_url = 'https://m.stock.naver.com/front-api/v1/news/category?category=mainnews&pageSize=50&page=1'

    resp_1 = requests.get(main_news_url)
    if (resp_1.status_code == 200) & resp_1.ok:
        main_news_list = json.loads(resp_1.text)['result']

        for main_news in main_news_list:
            news_id = main_news['officeId'] + main_news['articleId']
            body = main_news['body'][0:80] + '...'
            title = main_news['title']
            office_nm = main_news['officeName']
            if (news_id,) not in prev_data:
                data.append((news_id, office_nm, title, body, 'main'))
                result.append(news_id)

        sql = "INSERT INTO news (news_id,news_office_nm,news_title,news_content,news_type) VALUES (?,?,?,?,?)"
        try:
            mc.executemany(sql, data)
        except mysql.connector.Error as err:
            print("main Error:", err)
        mydb.commit()

    return result


def crawl_flash():
    """
    실시간 뉴스 크롤링 메소드 / news_id, 언론사, 제목, 내용 일부분, 뉴스 타입 저장
    :return: pk news_id 리스트 형식으로 리턴
    """
    find_all = "select news_id from news"
    try:
        mc.execute(find_all)
    except mysql.connector.Error as err:
        print('main find_all Error : ', err)
    prev_data = mc.fetchall()
    data = []
    result = []
    main_news_url = 'https://m.stock.naver.com/front-api/v1/news/category?category=flashnews&pageSize=50&page=1'

    resp_1 = requests.get(main_news_url)
    if (resp_1.status_code == 200) & resp_1.ok:
        main_news_list = json.loads(resp_1.text)['result']

        for main_news in main_news_list:
            news_id = main_news['officeId'] + main_news['articleId']
            body = main_news['body'][0:80] + '...'
            title = main_news['title']
            office_nm = main_news['officeName']
            if  (news_id,) not in prev_data:
                data.append((news_id, office_nm, title, body, 'flash'))
                result.append(news_id)
        sql = "INSERT INTO news (news_id,news_office_nm,news_title,news_content,news_type) VALUES (?,?,?,?,?)"
        try:
            mc.executemany(sql, data)
        except mysql.connector.Error as err:
            print("flash Error:", err)
            pass
        mydb.commit()

    return result


def crawl_news_detail(result):
    """
    pk news_id로 상세 내용 크롤링하는 메소드 / 작성일, 상세 내용 저장
    :param result: crawl_issue(), crawl_main(), crawl_flash()에서 리턴 받은 pk news_id 리스트
    :return: 완료 프린트
    """
    data = []
    for pk in result:

        oid = pk[0:3]
        aid = pk[3:]
        resp = requests.get(base_url + oid + '/' + aid)  # 요청
        # print(base_url + oid + '/' + aid)
        if (resp.status_code == 200) & resp.ok:
            soup = bs(resp.text, 'lxml')
            try:
                ct = soup.find('div', id='ct')
                content = ct.find('div', id='newsct_article')
                writer = ct.find('div', class_='byline')
                content_tag = content.__str__().replace('data-src', 'src')
                writer_tag = writer.__str__()
                tag = content_tag + writer_tag
                tag = tag.translate({ord(i): None for i in '\n'})
                date = ct.find('span', class_='_ARTICLE_DATE_TIME')['data-date-time']
                if bool(ct.find('span', class_='_ARTICLE_MODIFY_DATE_TIME')):
                    date = ct.find('span', class_='_ARTICLE_MODIFY_DATE_TIME')['data-modify-date-time']  # 뉴스 입력 시간
                data.append((date, tag, pk))
            except AttributeError:
                pass

    sql = "UPDATE news SET news_date = %s, news_tag = %s WHERE news_id = %s"
    try:
        mc.executemany(sql, data)
        mydb.commit()

    except mysql.connector.Error as err:
        print("detail Error:", err)
        pass

    return print("다 했다!")


def update_main_news():
    """
    주요 뉴스 업데이트 메소드 / 기존 주요 뉴스와 pk news_id로 중복 체크
    :return: 중복 제거된 pk news_id 집합으로 crawl_news_detail() 실행
    """
    sql = "select news_id from news where news_type = 'main'"
    try:
        mc.execute(sql)
    except mysql.connector.Error as err:
        print("Error:", err)
    data = mc.fetchall()
    results = crawl_main()
    new_main = []
    for result in results:
        if (result,) not in data:
            new_main.append(result)

    return crawl_news_detail(new_main)


def update_flash_news():
    """
    실시간 뉴스 업데이트 메소드 / 기존 실시간 뉴스와 pk news_id로 중복 체크
    :return: 중복 제거된 pk news_id 집합으로 crawl_news_detail() 실행
    """
    sql = "select news_id from news where news_type = 'flash'"
    try:
        mc.execute(sql)
    except mysql.connector.Error as err:
        print("Error:", err)
    data = mc.fetchall()
    results = crawl_flash()
    new_flash = []
    for result in results:
        if (result,) not in data:
            new_flash.append(result)

    return crawl_news_detail(new_flash)


if __name__ == '__main__':
    start = time.time()
    # keywords = crawl_issue_keywords()
    # issue_pk = crawl_issue(keywords)
    # main_pk = crawl_main()
    # flash_pk = crawl_flash()
    # crawl_news_detail(issue_pk)
    # crawl_news_detail(main_pk)
    # crawl_news_detail(flash_pk)

    update_issue()
    # update_main_news()
    # update_flash_news()
    print("time :", time.time() - start)
