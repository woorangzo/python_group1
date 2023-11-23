from django.test import TestCase

# Create your tests here.
import pandas as pd

# 데이터 프레임 생성
data = {'Name': ['John', 'Emma', 'Sam', 'Lisa'],
        'Age': [28, 32, 45, 36],
        'City': ['New York', 'London', 'Paris', 'Tokyo']}
df = pd.DataFrame(data)

# 데이터 프레임 출력
print(df)