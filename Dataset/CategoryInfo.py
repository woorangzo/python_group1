import csv
import mysql.connector
import requests


def get_category_data():
    api_url = 'https://datacenter.hankyung.com/equities-all/korea?type=kospi'
    api2_url = 'https://datacenter.hankyung.com/equities-all/korea?type=kosdaq'

    response = requests.get(api_url, verify=False)
    data = response.json()

    response2 = requests.get(api2_url, verify=False)
    data2 = response2.json()

    category_data = []

    if 'data' in data:
        for item in data['data']:
            category_nm = item.get('name')
            category_price = item.get('total_price')

            sub_list = item.get('sub', [])
            for sub_item in sub_list:
                stock_cd = sub_item.get('shortcode')
                if stock_cd:
                    category_data.append((stock_cd, category_nm, category_price))

    if 'data' in data2:
        for item in data2['data']:
            category_nm = item.get('name')
            category_price = item.get('total_price')

            sub_list = item.get('sub', [])
            for sub_item in sub_list:
                stock_cd = sub_item.get('shortcode')
                if stock_cd:
                    category_data.append((stock_cd, category_nm, category_price))

    return category_data


# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="woorangzo",
    passwd="1234",
    database="woorangzo"
)

mc = mydb.cursor()

sql = "INSERT INTO category_info (stock_cd, category_nm, category_total) VALUES (%s, %s, %s)"

category_data = get_category_data()

try:
    mc.executemany(sql, category_data)
    mydb.commit()
    print(mc.rowcount, "개의 레코드 입력")
except mysql.connector.Error as err:
    print("에러:", err)
    print("에러를 발생시킨 데이터:", category_data)
finally:
    mc.close()
    mydb.close()