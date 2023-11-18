import requests

import json
import pandas as pd


def get_price(code,name, n):
    url = 'http://finance.daum.net/api/charts/A%s/days?limit=%d&adjusted=true' % (code, n)

    headers = {

        'Accept': 'application/json, text/plain, */*',

        'Accept-Encoding': 'gzip, deflate',

        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',

        'Connection': 'keep-alive',

        'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',

        'Host': 'finance.daum.net',

        'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',

        'Referer': 'http://finance.daum.net/quotes/A069500',

        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

    }

    headers['Referer'] = 'http://finance.daum.net/quotes/A%s' % code

    r = requests.get(url, headers=headers)


    data = json.loads(r.text)

    df = pd.DataFrame(data['data'])

    df.index = pd.to_datetime(df['candleTime'])

    return df
# while(True) :
print(get_price('005930','삼성전자',5))
print("===================")
print(get_price('086520', '에코프로',10))
