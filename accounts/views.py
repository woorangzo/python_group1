from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse

from django.views.generic import TemplateView

from accounts.forms import JoinForm

from .models import Member
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import dates as mdates
import requests
import json
import pandas as pd
import os  # Import the os module for directory creati
import matplotlib

matplotlib.use('SVG')
from matplotlib import font_manager, rc  # 폰트 세팅을 위한 모듈 추가

font_path = "C:/Windows/Fonts/malgun.ttf"  # 사용할 폰트명 경로 삽입
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

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
