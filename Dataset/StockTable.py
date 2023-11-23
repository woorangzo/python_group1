import csv
import os
import mysql.connector

simp_path = "C:\\Users\\kitcoop\\Desktop\\samples"
abs_path = os.path.abspath(simp_path)


# 종목명과 코드 파싱
def process_file(file_path):
    file_name = os.path.basename(file_path)
    if "_" in file_name:
        items = file_name.split("_")
        if len(items) == 2:
            name, code = items[0], items[1].split(".")[0]
            return name, code


def valid_check(s_val):
    return float(s_val) if s_val else 0


# 해당 종목명과 코드와 일치하는 파일의 데이터를 반복문 돌면서 받아오기
def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        for row in csv_reader:
            data.append((code, row[0], valid_check(row[5]), valid_check(row[6]), valid_check(row[1]),
                         valid_check(row[4]), valid_check(row[2]), valid_check(row[3])))

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

        sql = "INSERT INTO stock (stock_cd, stock_dt, stock_volume, stock_rate, open_price, close_price, high_price, low_price) VALUES (%s, %s, IFNULL(%s,0), IFNULL(%s,0), IFNULL(%s,0), IFNULL(%s,0), IFNULL(%s,0), IFNULL(%s,0))"
        try:
            mc.executemany(sql, data)
        except mysql.connector.Error as err:
            print("Error:", err)
            print("Data causing the error:", data)

mydb.commit()
print(mc.rowcount, "개의 레코드 입력")
