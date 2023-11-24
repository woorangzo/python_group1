import csv
import os
import mysql.connector

simp_path = "C:/Users/woosw/OneDrive/바탕 화면/samples"
abs_path = os.path.abspath(simp_path)

# 주식 기본 정보 저장 (종목 코드, 종목 명)
def process_file(file_path):
    file_name = os.path.basename(file_path)
    if "_" in file_name:
        items = file_name.split("_")
        if len(items) == 2:
            name, code = items[0], items[1].split(".")[0]
            return name, code


def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        for row in csv_reader:
            data.append((code, name, row[7]))

            return data


files = os.listdir(abs_path)

mydb = mysql.connector.connect(
    host="localhost",
    user="woorangzo",
    passwd="1234",
    database="woorangzo"
)

mc = mydb.cursor()

for file_name in files:
    file_path = os.path.join(abs_path, file_name)

    name, code = process_file(file_path)
    if name is not None and code is not None:
        data = read_data_from_file(file_path)

        sql = "INSERT INTO stock_info (STOCK_CD, STOCK_NM, MARKET_TYPE) VALUES (%s, %s, %s)"
        try:
            mc.executemany(sql, data)
        except mysql.connector.Error as err:
            print("Error:", err)
            print("Data causing the error:", data)

mydb.commit()
print(mc.rowcount, "개의 레코드 입력")
