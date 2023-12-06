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

from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgun.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # TensorFlow의 DNN 옵션을 비활성화.

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
# stock_prediction 테이블 초기화
truncate_query = "TRUNCATE TABLE stock_prediction"
cursor = conn.cursor()
cursor.execute(truncate_query)
conn.commit()

# stock_info 테이블에서 모든 종목명 조회
all_stock_query = """
    SELECT DISTINCT stock_nm
    FROM stock_info
"""
all_stock_names = pd.read_sql(all_stock_query, conn)['stock_nm'].tolist()
selected_stock_names = all_stock_names


# 최근 1년치 데이터 선택 / 1년전 날짜 구하기
recent_data_start = pd.Timestamp.now() - pd.DateOffset(years=1)
recent_data_start_str = recent_data_start.strftime('%Y-%m-%d')

# 완료된 종목 수를 추적하는 completed_stocks 변수 초기화
completed_stocks = 0

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

    # 결측치 보간
    df.interpolate(method='linear', inplace=True)

    # 종가를 사용하여 스케일링 수행
    closing_prices = df['close_price'].values.reshape(-1, 1)
    scaled_data = closing_prices / closing_prices.max()  # 최대 종가로 스케일링

    # LSTM 모델 학습
    print(f"종목 '{stock_name}'의 LSTM 모델 학습 중...")
    lstm_model = train_lstm_model(scaled_data)
    print(f"종목 '{stock_name}'의 LSTM 모델 학습 완료.")

    completed_stocks += 1
    print(f"진행 상황: {completed_stocks}/{len(selected_stock_names)}")

    # 다음날 예측 수행
    print(f"종목 '{stock_name}'의 다음날 예측 중...")
    future_days = 1
    prediction = []
    last_sequence = scaled_data[-10:].reshape(1, 10, 1)

    for _ in range(future_days):
        next_day_prediction = lstm_model.predict(last_sequence)[0][0]
        prediction.append(next_day_prediction)
        last_sequence = np.append(last_sequence[:, 1:, :], [[[next_day_prediction]]], axis=1)

    # 역 스케일링을 통해 실제 예측된 종가 획득
    predicted_close = prediction[-1] * closing_prices.max()

    # 추가된 부분: 각 주식에 대한 정보를 한 번씩만 저장
    last_actual_close = df['close_price'].iloc[-1]  # 마지막 날 종가
    last_actual_stock_cd = df['stock_cd'].iloc[-1]  # 주식 코드
    last_actual_volume = df['stock_volume'].iloc[-1]  # 마지막 날 거래량

    change_rate = ((predicted_close - last_actual_close) / last_actual_close) * 100  # 등락률 계산

    # 이미지를 파일로 저장
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['close_price'], label='종가')

    next_day = df.index[-1] + pd.DateOffset(1)

    plt.plot(next_day, predicted_close, 'ro', label='다음날 예측 종가')  # 예측값 빨간 동그라미로 표시
    plt.axhline(y=last_actual_close, color='red', linestyle='--', label='마지막 종가')  # 마지막 종가 빨간 선(가로)으로 표시
    # plt.plot([df.index[-1], next_day], [last_actual_close, predicted_close], 'r--')  # 선으로 마지막 종가와 예측값 연결

    plt.xlabel('날짜')
    plt.ylabel('주가')
    plt.title(f"{stock_name}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    original_absolute_path = r'C:\kch\python\woorangzo\stock\stock\static\img'
    graph_filename = os.path.join(original_absolute_path, f"{stock_name}_prediction.png")
    plt.savefig(graph_filename)
    plt.close()  # 각 그래프 생성 후 닫기

    # 이미지 파일을 BLOB으로 읽기
    with open(graph_filename, 'rb') as file:
        binary_data = file.read()

    # stock_prediction 테이블에 한 번씩만 저장
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO stock_prediction (stock_nm, stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume, graph_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        stock_name, last_actual_stock_cd, last_actual_close, predicted_close, change_rate, last_actual_volume,
        graph_filename))

    # 커밋
    conn.commit()

# 모든 종목의 학습 및 예측이 완료된 후, n개 종목의 학습 예측 완료 메시지 출력
n = len(selected_stock_names)
print(f"{n}개 종목의 학습 및 예측이 완료되었습니다.")


