import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

# 내장된 나눔 폰트 사용
#plt.rcParams['font.family'] = 'NanumBarunGothic'

def get_price(code, name, n):
    url = f'http://finance.daum.net/api/charts/A{code}/days?limit={n}&adjusted=true'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    headers['Referer'] = f'http://finance.daum.net/quotes/A{code}'

    r = requests.get(url, headers=headers)
    data = json.loads(r.text)

    # 데이터가 없으면 None 반환
    if 'data' not in data:
        return None

    df = pd.DataFrame(data['data'])
    df.index = pd.to_datetime(df['candleTime'])

    return df

def plot_stock_prices(codes_and_names, n):
    plt.figure(figsize=(10, 6))

    for code, name in codes_and_names:
        data = get_price(code, name, n)

        # 데이터가 없는 경우 그래프를 그리지 않음
        if data is not None:
            returns = data['changeRate']
            plt.plot(data.index, returns, label=name)

    # 그래프 스타일 및 주요 설정
    plt.title('Stock Price Change Rate Comparison')
    plt.xlabel('Date')
    plt.ylabel('Change Rate (%)')
    plt.axhline(0, color='black', linestyle='--', linewidth=1, label='Zero Line')
    plt.legend()

    # Y축 눈금 설정 (세분화)
    y_ticks = [i/100 for i in range(-10, 11, 1)]  # -10%부터 10%까지 1% 간격
    plt.yticks(y_ticks)

    # X축 날짜 형식 설정
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # 그래프 보여주기
    plt.show()

# 사용자에게 종목 코드와 이름을 입력받기
codes_and_names = [
    ('023530', 'lotteshoping'),
    ('004170', 'shinsege'),
    ('057050', 'hydaihomeshoping')
]

# 그래프 그리기
plot_stock_prices(codes_and_names, 50)
