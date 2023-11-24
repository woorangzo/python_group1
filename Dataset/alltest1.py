import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# 종목 예측 차트 (종가, 거래량, 시가, 고가, 저가) #
# 종목명 검색 #
# 전 종목 학습 #

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='woorangzo',
    passwd='1234',
    db='woorangzo'
)



# SQL 쿼리 작성 - 모든 주식 데이터 조회 (종가, 거래량, 시가, 고가, 저가)
sql_query = """
    SELECT s.stock_cd, s.stock_dt, s.close_price, s.stock_volume, s.open_price, s.high_price, s.low_price
    FROM stock s
    ORDER BY s.stock_cd ASC, s.stock_dt ASC
"""


# DataFrame에 SQL 결과 저장
df = pd.read_sql(sql_query, conn)
df['stock_dt'] = pd.to_datetime(df['stock_dt'])
df = df.set_index('stock_dt')

# 주식 데이터 정규화
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df[['close_price', 'stock_volume', 'open_price', 'high_price', 'low_price']])

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
model.add(LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 5)))
model.add(LSTM(units=50))
model.add(Dense(units=5))  # 종가, 거래량, 시가, 고가, 저가

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x, y, epochs=100, batch_size=32)

# 'prediction' 리스트에는 각 주식에 대한 내일 예측값이 있어야 합니다.
# 'prediction'은 기존 코드에서 예측 부분을 수행한 결과일 것입니다.


# 다음날 주식 예측
future_days = 1
prediction = []
last_sequence = scaled_data[-sequence_length:]
last_sequence = last_sequence.reshape((1, sequence_length, 5))

for _ in range(future_days):
    next_day_prediction = model.predict(last_sequence)[0]
    prediction.append(next_day_prediction)
    last_sequence = np.append(last_sequence[:, 1:, :], [[next_day_prediction]], axis=1)
# 'prediction' 변수에 내일의 주식 가격 예측값이 저장됨


# 각 주식의 오늘과 내일 예측된 종가 차이를 계산합니다.
price_difference = []  # 주가 차이를 저장할 리스트

for i in range(len(df)):  # 각 주식에 대해 반복합니다.
    predicted_today = df.iloc[i]['close_price']  # 'df'는 원본 주식 데이터를 포함하는 DataFrame이라고 가정합니다
    predicted_tomorrow = scaler.inverse_transform(prediction[i].reshape(1, -1))[0][0]  # 'prediction'은 스케일된 값이라고 가정합니다

    difference = predicted_tomorrow - predicted_today
    price_difference.append((i, difference))  # 인덱스와 차이를 튜플 형태로 리스트에 추가합니다

# 주가 차이를 기준으로 주식을 정렬합니다.
top_5_stocks = sorted(price_difference, key=lambda x: x[1], reverse=True)[:5]

# 상위 5개 주식의 인덱스와 차이를 가져옵니다.
top_5_indices = [stock[0] for stock in top_5_stocks]
top_5_differences = [stock[1] for stock in top_5_stocks]

# 상위 5개 주식에 대한 정보를 가져옵니다.
top_5_stock_info = df.iloc[top_5_indices]  # 'df'는 원본 주식 데이터를 포함하는 DataFrame이라고 가정합니다

# 상위 5개 주식의 정보를 출력하거나 사용합니다.
print("내일 예측된 주가 상승이 가장 높은 상위 5개 주식:")
print(top_5_stock_info[['stock_cd', 'close_price']])
print("예측된 가격 상승폭:")
print(top_5_differences)

# MySQL 연결 종료
conn.close()
