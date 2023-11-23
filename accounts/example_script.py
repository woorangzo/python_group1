import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib import dates as mdates

# 한글 폰트 경로 설정 (본인 컴퓨터에 있는 한글 폰트 경로로 변경)
font_path = 'C:/Windows/Fonts/malgun.ttf'

# 한글 폰트 설정
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def get_price(code, name, n):
    url = 'http://finance.daum.net/api/charts/A%s/days?limit=%d&adjusted=true' % (code, n)

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    headers['Referer'] = 'http://finance.daum.net/quotes/A%s' % code

    r = requests.get(url, headers=headers)
    data = json.loads(r.text)

    # 데이터가 없으면 None 반환
    if 'data' not in data:
        return None

    df = pd.DataFrame(data['data'])
    df.index = pd.to_datetime(df['candleTime'])

    return df


def plot_stock_prices():
    # 데이터 가져오기
    samsung_data = get_price('005930', '삼성전자', 50)
    ecopro_data = get_price('086520', '에코프로', 50)

    # 데이터가 없는 경우 그래프를 그리지 않음
    if samsung_data is None or ecopro_data is None:
        print("No data available.")
        return

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.plot(samsung_data.index, samsung_data['tradePrice'], label='삼성전자')
    plt.plot(ecopro_data.index, ecopro_data['tradePrice'], label='에코프로')

    # 그래프 스타일 및 주요 설정
    plt.title('삼성전자 vs 에코프로 주식 가격 비교')
    plt.xlabel('일자')
    plt.ylabel('주가')
    plt.legend()

    # X축 날짜 형식 설정
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # 그래프 보여주기
    plt.show()


# 그래프 그리기
plot_stock_prices()
