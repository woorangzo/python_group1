import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='woorangzo',
    passwd='1234',
    db='woorangzo'
)

# 사용자로부터 종목명 5개 입력 받기
# 현재 에러
stocks_to_predict = []
for i in range(5):
    stock_name = input(f"종목명 {i+1}을 입력하세요: ")
    stocks_to_predict.append(stock_name)

for stock_name in stocks_to_predict:
    # SQL 쿼리 작성 - 종목명을 기준으로 데이터 조회
    sql_query = f"""
        SELECT s.stock_dt, s.close_price, s.stock_volume, s.open_price, s.high_price, s.low_price
        FROM stock s
        JOIN stock_info si ON s.stock_cd = si.stock_cd
        WHERE si.stock_nm = '{stock_name}'
        ORDER BY s.stock_dt ASC
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

    # LSTM 모델을 사용하여 다음날 데이터 예측
    last_sequence = scaled_data[-sequence_length:]
    last_sequence = np.expand_dims(last_sequence, axis=0)
    predicted = model.predict(last_sequence)
    predicted = scaler.inverse_transform(predicted)  # 역정규화

    # 다음날 예측 데이터를 DataFrame에 추가
    next_day = pd.to_datetime(df.index[-1]) + pd.DateOffset(1)
    next_day_data = [next_day] + list(predicted[0])
    df.loc[next_day] = next_day_data

    # Calculate actual and predicted values
    last_actual_close = df['close_price'].iloc[-2]  # Second to last value
    predicted_close = predicted[0][0]  # Predicted close price for the next day

    # Assuming the last_day_volume is the volume of the last day in your DataFrame
    last_day_volume = df['stock_volume'].iloc[-1]

    # Calculate percentage change
    percentage_change = ((predicted_close - last_actual_close) / last_actual_close) * 100
    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close_price'], label='Actual Close Price')
    plt.plot(df.index[-1], predicted[0][0], 'ro', label='Predicted Close Price')
    plt.title(f"{stock_name} - Next Day Prediction")
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.show()

    # Print information - 정보 출력
    print(f"Stock: {stock_name}")
    print(f"Last Day Close Price: {last_actual_close}")
    print(f"Predicted Close Price: {predicted_close}")
    print(f"Percentage Change: {percentage_change:.2f}%")
    print(f"Last Day Volume: {last_day_volume}")
    print("\n")

# MySQL 연결 종료
conn.close()
