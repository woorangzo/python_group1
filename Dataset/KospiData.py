import time
import schedule
from datetime import datetime
from pykrx import stock
import mysql.connector

# MySQL connection setup
mydb = mysql.connector.connect(
    host="localhost",
    user="woorangzo",
    passwd="1234",
    database="woorangzo"
)
cursor = mydb.cursor()

# Other setup (start_datetime, end_datetime, update_interval, etc.)
start_time = "09:00"
end_time = "16:00"
start_datetime = datetime.strptime(start_time, "%H:%M")
end_datetime = datetime.strptime(end_time, "%H:%M")
update_interval = 1

# Function to update data in the database
def update_data():
    try:
        current_date = datetime.now().strftime("%Y%m%d")
        kospi_data = stock.get_index_price_change(current_date, current_date, "KOSPI")
        kosdaq_data = stock.get_index_price_change(current_date, current_date, "KOSDAQ")

        if not kospi_data.empty:
            row_kospi = kospi_data.iloc[0]
            # print(row_kospi)
            insert_or_update_record('코스피', current_date, row_kospi)

        if not kosdaq_data.empty:
            row_kosdaq = kosdaq_data.iloc[0]
            print(row_kosdaq)
            insert_or_update_record('코스닥', current_date, row_kosdaq)

        print(f"Data updated for {current_date}")
        mydb.commit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def insert_or_update_record(index, current_date, row):
    try:
        cursor.execute('''
            INSERT INTO main_finance (main_nm, open_price, close_price, stock_rate, stock_volume, stock_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            open_price = VALUES(open_price),
            close_price = VALUES(close_price),
            stock_rate = VALUES(stock_rate),
            stock_volume = VALUES(stock_volume),
            stock_price = VALUES(stock_price)
        ''', (index, row['시가'], row['종가'], row['등락률'], row['거래량'], row['거래대금']))

        mydb.commit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Run the update_data function every second during the specified time range
while True:
    try:
        current_datetime = datetime.now().time()

        if start_datetime.time() <= current_datetime <= end_datetime.time():
            schedule.run_pending()
        else:
            print("Time range exceeded. Waiting for the next update time.")

        schedule.clear('update_data')
        schedule.every(update_interval).seconds.do(update_data).tag('update_data')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    time.sleep(update_interval)
