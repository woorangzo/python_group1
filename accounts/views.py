from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse


from django.views.generic import TemplateView

from accounts.forms import JoinForm


from .forms import StockInputForm
from .models import StockData, Member
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import dates as mdates
import requests
import json
import pandas as pd
import os  # Import the os module for directory creati
import matplotlib
matplotlib.use('SVG')
from matplotlib import font_manager, rc # 폰트 세팅을 위한 모듈 추가
font_path = "C:/Windows/Fonts/malgun.ttf" # 사용할 폰트명 경로 삽입
font = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font)

plt.rc('axes', unicode_minus=False)

# Create your views here.
def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            member_data = form.cleaned_data
            if member_data['member_pw'] == member_data['member_repw']:
                Member.objects.create(
                    member_id=member_data['member_id'],
                    member_pw=member_data['member_pw'],
                    member_repw=member_data['member_repw'],
                    username=member_data['username'],
                    phone=member_data['phone'],
                    email=member_data['email'],
                    jumin=member_data['jumin']
                )
                return redirect('accounts:login')
            else:
                form.add_error('member_repw', '비밀번호가 일치하지 않습니다')
    else:
        form = JoinForm()

    return render(request, 'accounts/join.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('singlepage:index')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('home')
    return render(request,'accounts/join.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('home')
    return render(request, 'accounts/join.html')


def mainview(request):
    return render(request, 'accounts/index.html')


def blank(request):
    return render(request, 'accounts/blank.html')


def mypage(request):
    return render(request, 'accounts/mypage.html')


def relatedStocks(request):
    return render(request, 'accounts/relatedStocks.html')

def issue(request):
    return render(request, 'accounts/issue.html')


def stockRecommend(request):
    return render(request, 'accounts/stockRecommend.html')


def news(request):
    return render(request, 'accounts/news.html')

def analyze(request):
    return render(request, 'accounts/analyze.html')


def theme(request):
    return render(request, 'accounts/theme.html')

def calc(request):
    return render(request, 'accounts/calc.html')

def get_price(code, name, n):
    url = f'http://finance.daum.net/api/charts/A{code}/days?limit={n}&adjusted=true'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    headers['Referer'] = f'http://finance.daum.net/quotes/A{code}'

    r = requests.get(url, headers=headers)
    data = json.loads(r.text)

    # 데이터가 없으면 None 반환
    if 'data' not in data:
        return None

    df = pd.DataFrame(data['data'])
    df.index = pd.to_datetime(df['candleTime'])

    return df

def plot_stock_prices(request):
    stock_info_list = []

    if request.method == 'POST':
        form = StockInputForm(request.POST)
        if form.is_valid():
            # Split the input codes and names, and remove leading/trailing whitespaces
            codes = [item.strip() for item in form.cleaned_data['codes'].split(',')]
            names = [item.strip() for item in form.cleaned_data['names'].split(',')]

            if len(codes) != len(names):
                return render(request, 'accounts/plot_stock_prices.html', {'plot_path': None, 'error': 'Mismatched number of codes and names.'})

            n = 50
            plt.figure(figsize=(10, 6))

            for code, name in zip(codes, names):
                data = get_price(code, name, n)

                if data is not None:
                    returns = data['changeRate']
                    plt.plot(data.index, returns, label=name)

                    stock_info_list.append({
                        'code': code,
                        'name': name,
                        'change_rate': data['changeRate'].tolist(),

                    })

                    # 데이터를 모델에 저장
                    for index, row in data.iterrows():
                        StockData.objects.create(
                            code=code,
                            name=name,
                            date=index,
                            change_rate=row['changeRate'],

                        )

            plt.title('주식 등락률 비교')
            plt.xlabel('일자')
            plt.ylabel('등락률(%)')
            plt.axhline(0, color='black', linestyle='--', linewidth=1, label='Zero Line')
            plt.legend()

            y_ticks = [i / 100 for i in range(-10, 11, 1)]
            plt.yticks(y_ticks)

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # 그래프 저장
            plot_path = "./accounts/static/pic/stock_plot.png"

            # 디렉토리 생성
            os.makedirs(os.path.dirname(plot_path), exist_ok=True)

            plt.savefig(plot_path)
            plt.close()

            return render(request, 'accounts/plot_stock_prices.html', {'plot_path': plot_path,
                                                                       'stock_info_list': stock_info_list,})

    else:
        form = StockInputForm()


    return render(request, 'accounts/plot_stock_prices.html', {'form': form})



def plot_get_stock_prices(request):
    stock_info_list = []

    if request.method == 'POST':
        form = StockInputForm(request.POST)
        if form.is_valid():
            # Split the input codes and names, and remove leading/trailing whitespaces
            codes = [item.strip() for item in form.cleaned_data['codes'].split(',')]
            names = [item.strip() for item in form.cleaned_data['names'].split(',')]

            if len(codes) != len(names):
                return render(request, 'accounts/plot_stock_prices.html', {'plot_path': None, 'error': 'Mismatched number of codes and names.'})

            n = 50
            plt.figure(figsize=(10, 6))

            for code, name in zip(codes, names):
                data = get_price(code, name, n)

                if data is not None:
                    stock_info_list.append({
                        'code': code,
                        'name': name,
                        'trade_price': data['tradePrice'].tolist(),
                    })

                    # 데이터를 모델에 저장
                    for index, row in data.iterrows():
                        StockData.objects.create(
                            code=code,
                            name=name,
                            date=index,
                            trade_price=row['tradePrice'],
                        )

                    # Plot stock price on the left y-axis
                    plt.plot(data.index, data['tradePrice'], label=f"{name} 주가")

                    # 여기에 주가 예측을 위한 코드를 추가하고 예측 그래프를 생성하여 저장
                    # 예시로 prediction_image 필드를 사용하겠습니다.
                    # prediction_image에는 주가 예측을 위한 이미지 파일의 경로를 저장하도록 합니다.
                    StockData.objects.filter(code=code, name=name).update(prediction_image=prediction_image_path)

            # 그래프 스타일 및 주요 설정
            plt.title('주식 주가 비교')
            plt.xlabel('일자')
            plt.ylabel('주가')
            plt.legend(loc='upper left')  # 위치 조정

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # 그래프 저장
            plot_path = "./accounts/static/pic/stock_price_plot.png"
            os.makedirs(os.path.dirname(plot_path), exist_ok=True)
            plt.savefig(plot_path)
            plt.close()

            return render(request, 'accounts/plot_stock_prices.html', {'plot_path': plot_path,
                                                                      'stock_info_list': stock_info_list,})

    else:
        form = StockInputForm()

    return render(request, 'accounts/plot_stock_prices.html', {'form': form})

def plot_get_stock_prices(request):
    stock_info_list = []

    if request.method == 'POST':
        form = StockInputForm(request.POST)
        if form.is_valid():
            codes = [item.strip() for item in form.cleaned_data['codes'].split(',')]
            names = [item.strip() for item in form.cleaned_data['names'].split(',')]

            if len(codes) != len(names):
                return render(request, 'accounts/plot_stock_prices.html', {'plot_path': None, 'error': '코드와 이름의 수가 일치하지 않습니다.'})

            n = 50
            plt.figure(figsize=(10, 6))

            for code, name in zip(codes, names):
                # 데이터베이스에서 주식 정보 가져오기
                stock_data = StockData.objects.filter(stock_cd=code).order_by('stock_dt')[:n]
                if not stock_data.exists():
                    continue

                # Pandas DataFrame으로 변환
                data = pd.DataFrame(list(stock_data.values()))
                data['stock_dt'] = pd.to_datetime(data['stock_dt'])
                data.set_index('stock_dt', inplace=True)

                stock_info_list.append({
                    'code': code,
                    'name': name,
                    'trade_price': data['close_price'].tolist(),  # 종가를 사용
                    'change_rate': data['stock_rate'].tolist(),
                })