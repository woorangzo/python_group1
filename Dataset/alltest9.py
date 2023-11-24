import random

import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 스케일링 방식 매일매일을 종가로 나누기 #
# 기간을 고려하지않고 #
# 매일매일의 가격 관련 지표를 전날의 종가에 대비하여 스케일링 #

# MySQL 연결
conn = pymysql.connect(
    host='localhost',
    user='woorangzo',
    passwd='1234',
    db='woorangzo'
)

# 종목명 가져오기
all_stock_query = """
    SELECT DISTINCT stock_nm
    FROM stock_info
"""
# 종목명 가져오기
all_stock_names = pd.read_sql(all_stock_query, conn)['stock_nm'].tolist()

# 무작위로 100개의 종목 선택
random.seed(42)  # 일정한 결과를 얻기 위해 시드 설정
selected_stock_names = random.sample(all_stock_names, 10)

# 모든 종목에 대한 가격 변동률 정보 저장할 리스트
all_stock_changes = []

for stock_name in selected_stock_names:
    # 종목명에 해당하는 데이터 검색
    sql_query = f"""
        SELECT s.stock_dt, s.close_price, s.stock_volume, s.open_price, s.high_price, s.low_price, si.stock_cd, si.stock_nm
        FROM stock s
        JOIN stock_info si ON s.stock_cd = si.stock_cd
        WHERE si.stock_nm = '{stock_name}'
        ORDER BY s.stock_dt ASC
    """

    # DataFrame에 SQL 결과 저장
    df = pd.read_sql(sql_query, conn)
    df['stock_dt'] = pd.to_datetime(df['stock_dt'])
    df = df.set_index('stock_dt')

    # 종가를 사용하여 스케일링 수행
    closing_prices = df['close_price'].values.reshape(-1, 1)
    scaled_data = closing_prices / closing_prices.max()  # 최대 종가로 스케일링

    def create_sequences(data, seq_length):
        x, y = [], []
        for i in range(len(data) - seq_length):
            x.append(data[i:(i + seq_length)])
            y.append(data[i + seq_length])
        return np.array(x), np.array(y)

    # 시퀀스 길이 정의 및 시퀀스 생성
    sequence_length = 10
    x, y = create_sequences(scaled_data, sequence_length)

    # LSTM 모델 생성 및 학습
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x, y, epochs=100, batch_size=32)

    # 다음날 예측 수행
    future_days = 1
    prediction = []
    last_sequence = scaled_data[-sequence_length:].reshape(1, sequence_length, 1)

    for _ in range(future_days):
        next_day_prediction = model.predict(last_sequence)[0][0]
        prediction.append(next_day_prediction)
        last_sequence = np.append(last_sequence[:, 1:, :], [[[next_day_prediction]]], axis=1)

    # 역 스케일링을 통해 실제 예측된 종가 획득
    predicted_close = prediction[-1] * closing_prices.max()

    # 추가된 부분: 각 주식에 대한 정보 출력
    last_actual_close = df['close_price'].iloc[-1]  # 마지막 날 종가
    last_actual_stock_cd = df['stock_cd'].iloc[-1]  # 주식 코드
    last_actual_volume = df['stock_volume'].iloc[-1]  # 마지막 날 거래량

    percentage_change = ((predicted_close - last_actual_close) / last_actual_close) * 100  # 가격 변동률 계산

    # 종목별 정보를 튜플로 저장
    stock_info = (stock_name, last_actual_close, predicted_close, percentage_change, last_actual_volume)
    all_stock_changes.append(stock_info)

# 가격 변동률 기준 내림차순으로 정렬
sorted_stock_changes = sorted(all_stock_changes, key=lambda x: x[3], reverse=True)

# 상위 5개 종목 정보 출력 (위치 변경)
top_5_stocks = sorted_stock_changes[:5]
for idx, stock in enumerate(top_5_stocks, start=1):
    stock_name, last_actual_close, predicted_close, percentage_change, last_actual_volume = stock
    print(f"Top {idx} 종목 이름: {stock_name}")
    print(f"종목 코드: {last_actual_stock_cd}")
    print(f"마지막 날 종가: {last_actual_close}")
    print(f"예측된 다음 날 종가: {predicted_close}")
    print(f"가격 변동률: {percentage_change:.2f}%")
    print(f"마지막 날 거래량: {last_actual_volume}")
    print("\n")

# MySQL 연결 종료
conn.close()
