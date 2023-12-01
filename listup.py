import warnings
warnings.filterwarnings("ignore") # warnings 모듈 사용하여 경고 메시지 무시

import os
import random
import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # TensorFlow의 DNN 옵션을 비활성화

# LSTM 모델 학습을 위한 함수 정의
def train_lstm_model(data):
    sequence_length = 10
    x, y = create_sequences(data, sequence_length)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x, y, epochs=100, batch_size=32)

    return model

# 데이터 시퀀스 생성 함수
def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length):
        x.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(x), np.array(y)

# MySQL 연결
conn = pymysql.connect(
    host='localhost',
    user='woorangzo',
    passwd='1234',
    db='woorangzo'
)

# 데이터 초기화
# stock_predictions 테이블 초기화
truncate_query = "TRUNCATE TABLE stock_predictions"
cursor = conn.cursor()
cursor.execute(truncate_query)
conn.commit()

# stock_info 테이블에서 종목명 조회
# 종목 무작위 선택
all_stock_query = """
    SELECT DISTINCT stock_nm
    FROM stock_info
"""
all_stock_names = pd.read_sql(all_stock_query, conn)['stock_nm'].tolist()
random.seed(42)  # 일정한 결과를 얻기 위해 시드 설정
selected_stock_names = random.sample(all_stock_names, 10) # 종목 무작위 선택 개수

# 모든 종목에 대한 가격 변동률 정보 저장할 리스트
all_stock_changes = []

# 최근 1년치 데이터 선택 / 1년전 날짜 구하기
recent_data_start = pd.Timestamp.now() - pd.DateOffset(years=1)
recent_data_start_str = recent_data_start.strftime('%Y-%m-%d')

# 모든 종목에 대한 학습 및 예측
for stock_name in selected_stock_names:
    # 종목명에 해당하는 최근 1년치 데이터 검색
    sql_query = f"""
            SELECT s.stock_dt, s.close_price, s.stock_volume, s.open_price, s.high_price, s.low_price, si.stock_cd, si.stock_nm
            FROM stock s
            JOIN stock_info si ON s.stock_cd = si.stock_cd
            WHERE si.stock_nm = '{stock_name}' AND s.stock_dt >= '{recent_data_start_str}'
            ORDER BY s.stock_dt ASC
        """

    # DataFrame에 SQL 결과 저장
    df = pd.read_sql(sql_query, conn)
    df['stock_dt'] = pd.to_datetime(df['stock_dt'])
    df = df.set_index('stock_dt')

    # 종가를 사용하여 스케일링 수행
    closing_prices = df['close_price'].values.reshape(-1, 1)
    scaled_data = closing_prices / closing_prices.max()  # 최대 종가로 스케일링

    # LSTM 모델 학습
    lstm_model = train_lstm_model(scaled_data)

    # 다음날 예측 수행
    future_days = 1
    prediction = []
    last_sequence = scaled_data[-10:].reshape(1, 10, 1)

    for _ in range(future_days):
        next_day_prediction = lstm_model.predict(last_sequence)[0][0]
        prediction.append(next_day_prediction)
        last_sequence = np.append(last_sequence[:, 1:, :], [[[next_day_prediction]]], axis=1)

    # 역 스케일링을 통해 실제 예측f된 종가 획득
    predicted_close = prediction[-1] * closing_prices.max()

    # 추가된 부분: 각 주식에 대한 정보를 한 번씩만 저장
    last_actual_close = df['close_price'].iloc[-1]  # 마지막 날 종가
    last_actual_stock_cd = df['stock_cd'].iloc[-1]  # 주식 코드
    last_actual_volume = df['stock_volume'].iloc[-1]  # 마지막 날 거래량

    change_rate = ((predicted_close - last_actual_close) / last_actual_close) * 100  # 등락률 계산

    # 이미지를 파일로 저장
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['close_price'], label='Actual Close Price')

    next_day = df.index[-1] + pd.DateOffset(1)

    plt.plot(next_day, predicted_close, 'ro', label='Predicted Close Price')  # 예측값 빨간 동그라미로 표시
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f"Stock Price Prediction for {stock_name}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    absolute_path = r'C:\kch\python\woorangzo\stock\stock\static\img'
    graph_filename = os.path.join(absolute_path, f"{stock_name}_prediction.png")
    plt.savefig(graph_filename)
    plt.close()  # 각 그래프 생성 후 닫기

    # 이미지 파일을 BLOB으로 읽기
    with open(graph_filename, 'rb') as file:
        binary_data = file.read()

    # stock_predictions 테이블에 한 번씩만 저장
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO stock_predictions (stock_nm, stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume, graph_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        stock_name, last_actual_stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume,
        graph_filename))

    # 커밋
    conn.commit()

# 가격 변동률 기준 내림차순으로 정렬
sorted_stock_changes = sorted(all_stock_changes, key=lambda x: x[4], reverse=True)

# 모든 종목 정보를 데이터베이스에 저장
for stock in sorted_stock_changes:
    stock_name, last_actual_stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume, graph_filename = stock

    # SQL INSERT 문 실행
    insert_query = f"""
                    INSERT INTO stock_predictions (stock_nm, stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume, graph_path)
                    VALUES ('{stock_name}', '{last_actual_stock_cd}', {last_actual_close}, {predicted_close}, {change_rate}, {last_actual_volume}, '{graph_filename}')
                """

    # 쿼리 실행
    cursor.execute(insert_query)

# 커밋
conn.commit()

# 모든 종목 정보
for idx, stock in enumerate(sorted_stock_changes, start=1):
    stock_name, last_actual_stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume, graph_filename = stock
    # print(f"종목 이름: {stock_name}")
    # print(f"종목 코드: {last_actual_stock_cd}")
    # print(f"마지막 날 종가: {last_actual_close}")
    # print(f"예측된 다음 날 종가: {predicted_close}")
    # print(f"예측 등락률: {change_rate:.2f}%")  # 예측 등락률 출력
    # print(f"마지막 날 거래량: {last_actual_volume}")
    # print("\n")

    # plt.show()


def get_sorted_stock_changes():
    return sorted_stock_changes

# MySQL 연결 종료
conn.close()



