import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# 모든 종목 학습 예측 #

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='woorangzo',
    passwd='1234',
    db='woorangzo'
)

# 사용자로부터 종목 코드 입력 받기
stock_name = input("종목명을 입력하세요: ")

# SQL 쿼리 작성 - 종목명을 기준으로 데이터 조회
# (종가, 거래량, 시가, 고가, 저가)
sql_query = f"""
    SELECT s.stock_dt, s.close_price, s.stock_volume, s.open_price, s.high_price, s.low_price, si.stock_cd, si.stock_nm
    FROM stock s
    JOIN stock_info si ON s.stock_cd = si.stock_cd
    ORDER BY si.stock_cd ASC, s.stock_dt ASC
"""


# DataFrame에 SQL 결과 저장
df = pd.read_sql(sql_query, conn)
df['stock_dt'] = pd.to_datetime(df['stock_dt'])
df = df.set_index('stock_dt')

# 주식 데이터 정규화
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df[['close_price', 'stock_volume', 'open_price', 'high_price', 'low_price', 'stock_cd']])

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
model.add(LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 6)))  # 6개의 속성을 가지고 있음 (종가, 거래량, 시가, 고가, 저가, stock_cd)
model.add(LSTM(units=50))
model.add(Dense(units=6))  # 종가, 거래량, 시가, 고가, 저가, stock_cd

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x, y, epochs=100, batch_size=32)

# 다음날 주식 예측
future_days = 1
prediction = []
last_sequence = scaled_data[-sequence_length:]
last_sequence = last_sequence.reshape((1, sequence_length, 6))

for _ in range(future_days):
    next_day_prediction = model.predict(last_sequence)[0]
    prediction.append(next_day_prediction)
    last_sequence = np.append(last_sequence[:, 1:, :], [[next_day_prediction]], axis=1)


# 마지막 예측값을 DataFrame에 추가
last_prediction = scaler.inverse_transform(prediction)[-1][0]
last_prediction_date = df.index[-1]  # 마지막 예측값의 날짜
df.loc[last_prediction_date, 'Prediction'] = last_prediction

last_actual_close = df['close_price'].iloc[-2]  # 끝에서 두 번째 값 (마지막 날 종가)
predicted_close = last_prediction  # 다음 날 종가 예측값

# 마지막 날 실제 거래량
last_actual_volume = df['stock_volume'].iloc[-2]  # 데이터프레임의 끝에서 두 번째 날 거래량 가져오기

# (다음날 종가 예측 - 데이터 마지막 날 종가) / 데이터 마지막 날 종가 (백분율)
percentage_change = ((predicted_close - last_actual_close) / last_actual_close) * 100

# 예측 결과를 원래 주식 데이터와 함께 그래프에 추가하여 그리기
future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=future_days)  # 11월 17일 이후의 날짜 생성
df_future = pd.DataFrame(index=future_dates, columns=df.columns)
df = pd.concat([df, df_future])  # 예측할 날짜까지 데이터 확장

# 주식 데이터 그래프 생성
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['close_price'], label='Actual Close Price')
plt.plot(df.index[-1], last_prediction, 'ro', label='Predicted Close Price')  # 예측값 빨간 동그라미로 표시
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title(f"Stock Price Prediction for {stock_name}")
plt.legend()
plt.grid(True)
plt.tight_layout()

# 마지막날 종가 및 종목 코드 접근
# last_actual_close = df['close_price'].iloc[-2]
last_actual_stock_cd = df['stock_cd'].iloc[-2]

# Print information - 정보 출력
print(f"종목 이름: {stock_name}")
print(f"종목 코드: {last_actual_stock_cd}")
print(f"마지막 날 종가: {last_actual_close}")
print(f"예측된 다음 날 종가: {predicted_close}")
print(f"가격 변동률: {percentage_change:.2f}%")
print(f"마지막 날 거래량: {last_actual_volume}")
print("\n")

# 그래프 표시
plt.show()

# MySQL 연결 종료
conn.close()