import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 종목 차트 보기 #
# 종목 코드 검색 #

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='woorangzo',
    passwd='1234',
    db='woorangzo'
)

# 사용자로부터 종목 코드 입력 받기
stock_code = input("종목 코드를 입력하세요: ")

# SQL 쿼리 작성 - 종목 코드를 기준으로 데이터 조회
sql_query = f"SELECT stock_dt, close_price FROM stock WHERE stock_cd = '{stock_code}'"

# DataFrame에 SQL 결과 저장
df = pd.read_sql(sql_query, conn)

# 종목 코드에 해당하는 데이터가 없는 경우 메시지 출력 후 종료
if df.empty:
    print(f"종목 코드 '{stock_code}'에 대한 데이터가 없습니다.")
else:
    # 차트 그리기
    df['stock_dt'] = pd.to_datetime(df['stock_dt'])  # stock_dt를 날짜로 변환
    df = df.set_index('stock_dt')  # 날짜를 인덱스로 설정

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close_price'], label='Close Price', marker='o', linestyle='-', color='b')
    plt.title(f"{stock_code} Close Price")
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend(loc='upper left')

    # x축 날짜 포맷 지정
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # x축 간격을 월 단위로 지정
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # x축 날짜 형식 지정
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator())  # 보조 눈금을 일 단위로 지정

    plt.xticks(rotation=45)  # x축 눈금 레이블 회전
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# MySQL 연결 종료
conn.close()
