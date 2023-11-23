import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# 종목 예측 차트 (종가) #
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
sql_query = f"SELECT stock_dt, close_price FROM stock WHERE stock_cd = '{stock_code}' ORDER BY stock_dt ASC"

# DataFrame에 SQL 결과 저장
df = pd.read_sql(sql_query, conn)
df['stock_dt'] = pd.to_datetime(df['stock_dt'])
df = df.set_index('stock_dt')

# 예측을 위한 데이터 전처리
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df['close_price'].values.reshape(-1, 1))

# LSTM 입력 데이터 생성 (시퀀스 형태로 변환)
def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length):
        x.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(x), np.array(y)

sequence_length = 10  # 시퀀스 길이 설정
x, y = create_sequences(scaled_data, sequence_length)

# LSTM 모델 생성 및 학습
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x, y, epochs=100, batch_size=32)

# 다음날 주식 예측
future_days = 1
prediction = []
last_sequence = scaled_data[-sequence_length:]
last_sequence = last_sequence.reshape((1, sequence_length, 1))

for _ in range(future_days):
    next_day_prediction = model.predict(last_sequence)[0]
    prediction.append(next_day_prediction)
    last_sequence = np.append(last_sequence[:, 1:, :], [[next_day_prediction]], axis=1)

# 예측 결과를 원래 주식 데이터와 함께 그래프에 추가하여 그리기
future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=future_days)  # 11월 17일 이후의 날짜 생성
df_future = pd.DataFrame(index=future_dates, columns=df.columns)
df = pd.concat([df, df_future])  # 예측할 날짜까지 데이터 확장
df['Prediction'] = np.nan
df.iloc[-future_days:, df.columns.get_loc('Prediction')] = scaler.inverse_transform(prediction)

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['close_price'], label='Original Data', marker='o', linestyle='-', color='b')
plt.plot(df.index[-future_days:], df['Prediction'].tail(future_days), label='Next Day Prediction', marker='o', linestyle='-', color='r')
plt.title(f"{stock_code} Next Day Prediction")
plt.xlabel('Day')
plt.ylabel('Close Price')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

# MySQL 연결 종료
conn.close()
