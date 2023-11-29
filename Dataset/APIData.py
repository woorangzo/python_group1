import time
import schedule
from datetime import datetime
from pykrx import stock
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="woorangzo",
    passwd="1234",
    database="woorangzo"
)
cursor = mydb.cursor()

# No need to create the table if it already exists

def record_exists(stock_cd):
    # Check if the record with the given stock_cd exists
    cursor.execute('SELECT COUNT(*) FROM daily_price WHERE stock_cd = %s', (str(stock_cd),))
    count = cursor.fetchone()[0]
    return count > 0

def insert_or_update_record(stock_cd, current_date, row):
    # Check if the record exists
    if record_exists(stock_cd):
        # Update the existing record
        update_existing_record(stock_cd, current_date, row)
    else:
        # Insert a new record
        insert_new_record(stock_cd, current_date, row)

def update_existing_record(stock_cd, current_date, row):
    cursor.execute('''
        UPDATE daily_price
        SET stock_dt=%s, open_price=%s, high_price=%s, low_price=%s,
        close_price=%s, stock_volume=%s, stock_rate=%s
        WHERE stock_cd=%s
    ''', (current_date, row['시가'], row['고가'], row['저가'], row['종가'], row['거래량'], row['등락률'], str(stock_cd)))

def insert_new_record(stock_cd, current_date, row):
    cursor.execute('''
        INSERT INTO daily_price (stock_cd, stock_dt, open_price, high_price, low_price, close_price, stock_volume, stock_rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (str(stock_cd), current_date, row['시가'], row['고가'], row['저가'], row['종가'], row['거래량'], row['등락률']))

def update_data():
    current_date = datetime.now().strftime("%Y%m%d")


    df_kospi = stock.get_market_ohlcv(current_date, market="KOSPI")
    df_kosdaq = stock.get_market_ohlcv(current_date, market="KOSDAQ")
    # df_Kospicap = stock.get_market_cap(current_date,current_date, market="KOSPI")
    # df_Kosdaqcap = stock.get_market_cap(current_date,current_date, market="KOSDAQ")

    for index, row in df_kospi.iterrows():
        insert_or_update_record(index, current_date, row)

    for index, row in df_kosdaq.iterrows():
        insert_or_update_record(index, current_date, row)

    print(f"Data updated for {current_date}")
    mydb.commit()

# 주식 조회시간 : 09~16:00까지
start_time = "09:00"
end_time = "16:00"

start_datetime = datetime.strptime(start_time, "%H:%M")
end_datetime = datetime.strptime(end_time, "%H:%M")

# 1초마다 갱신되게 설정
update_interval = 1

# 스케줄러 사용해서 지정한 시간과 날짜에 맞춰서 업데이트 되도록 설정
schedule.every(update_interval).seconds.do(update_data).tag('update_data')

while True:
    try:
        current_datetime = datetime.now().time()

        if start_datetime.time() <= current_datetime <= end_datetime.time():
            schedule.run_pending()
        else:
            print("시간 범위 초과")
            schedule.clear('update_data')
            schedule.every().day.at(start_time).do(update_data).tag('update_data')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    time.sleep(update_interval)
