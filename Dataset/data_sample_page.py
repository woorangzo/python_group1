from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Selenium 웹 드라이버 설정 (ChromeDriver 사용)
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# 웹페이지 열기
driver.get('http://127.0.0.1:8000/accounts/analyze/')

# 각 업종별로 탭 클릭 및 데이터 가져오기
for sector_id in ['left1', 'left2', 'left3', 'left4', 'left5']:
    # 업종 탭 클릭
    driver.execute_script(f"showleft('{sector_id}', event)")

    # 페이지 로딩을 위해 충분한 대기 시간 부여
    time.sleep(2)

    # 현재 페이지의 HTML 가져오기
    html = driver.page_source

    # BeautifulSoup을 사용하여 HTML을 파싱
    soup = BeautifulSoup(html, 'html.parser')

    # 데이터 추출 및 출력 (예시)
    print(f"Data for {sector_id}:")
    table = soup.find('table', class_='singnal')
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        종목명 = columns[0].text.strip()
        현재가 = columns[1].text.strip()
        전일비 = columns[2].text.strip()
        등락률 = columns[3].text.strip()
        print(f"종목명: {종목명}, 현재가: {현재가}, 전일비: {전일비}, 등락률: {등락률}")

# Selenium 웹 드라이버 종료
driver.quit()