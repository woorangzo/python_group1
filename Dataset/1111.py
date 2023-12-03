import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor

# MySQL 연결 설정 (SQLAlchemy 사용)
engine = create_engine('mysql+pymysql://woorangzo:1234@localhost/woorangzo')

# 종목 코드 리스트를 데이터베이스에서 가져오기
stock_codes_query = "SELECT DISTINCT stock_cd FROM stock_info"
stock_codes_df = pd.read_sql(stock_codes_query, engine)
stock_codes = stock_codes_df['stock_cd'].tolist()

# 결과를 저장할 빈 DataFrame 생성
result_df = pd.DataFrame()

# 각 종목에 대한 예측 및 결과 수집
for stock_code in stock_codes:
    # SQL 쿼리 작성 - 종목 코드를 기준으로 데이터 조회 (2023-11-01 이후의 데이터만)
    sql_query = f"SELECT stock_dt, close_price FROM stock WHERE stock_cd = '{stock_code}' AND stock_dt >= '2023-11-01'"

    # DataFrame에 SQL 결과 저장
    df = pd.read_sql(sql_query, engine)

    # 종목 코드에 해당하는 데이터가 없는 경우 메시지 출력 후 종료
    if df.empty:
        print(f"종목 코드 '{stock_code}'에 대한 2023-11-01 이후 데이터가 없습니다.")
    else:
        # 날짜를 인덱스로 설정
        df['stock_dt'] = pd.to_datetime(df['stock_dt'])
        df = df.set_index('stock_dt')

        # Feature Engineering: 날짜를 기반으로 한 특성 추가 (예: 요일, 주 등)
        df['day_of_week'] = df.index.dayofweek
        df['week'] = df.index.isocalendar().week  # 'week' 속성을 'isocalendar()' 메서드로 대체

        # 머신러닝 모델을 위한 특성과 타겟 데이터 생성
        X = df.drop('close_price', axis=1)
        y = df['close_price']

        # RandomForestRegressor 모델 학습
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # 전체 데이터에 대한 예측값
        y_pred = model.predict(X)

        # predicted_rise 열 계산
        df['predicted_rise'] = ((y_pred - df['close_price'].shift(1)) / df['close_price'].shift(1)) * 100

        # 종목 코드 추가
        df['stock_cd'] = stock_code

        # 결과를 전체 DataFrame에 추가
        result_df = pd.concat([result_df, df])

# 상승률이 가장 높은 상위 5개 주식 선택
top_5_stocks = result_df.nlargest(5, 'predicted_rise')

# 결과 출력 (종목명을 포함하여 출력)
stock_info_query = "SELECT stock_cd, stock_nm FROM stock_info"
stock_info_df = pd.read_sql(stock_info_query, engine)
top_5_stocks = pd.merge(top_5_stocks, stock_info_df, how='left', on='stock_cd')
print(f"내일 예측된 주가 상승률이 가장 높은 상위 5개 주식:")
print(top_5_stocks[['stock_nm', 'close_price', 'predicted_rise']])
# MySQL 연결 종료
engine.dispose()
