import pymysql
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# from sklearn.preprocessing import MinMaxScaler

# 100개 종목 학습 예측 #

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='woorangzo',
    passwd='1234',
    db='woorangzo'
)

# SQL 쿼리 작성 - 종목명을 기준으로 데이터 조회
# (종가, 거래량, 시가, 고가, 저가)
sql_query = """
    SELECT s.stock_dt, s.close_price, s.stock_volume, s.open_price, s.high_price, s.low_price, si.stock_cd, si.stock_nm
    FROM stock s
    JOIN stock_info si ON s.stock_cd = si.stock_cd
    ORDER BY RAND()
    LIMIT 10
"""


# DataFrame에 SQL 결과 저장
df = pd.read_sql(sql_query, conn)
print(df.isnull())
# df.dropna(axis=0)
# df['stock_dt'] = pd.to_datetime(df['stock_dt'])
# df = df.set_index('stock_dt')