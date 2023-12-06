import random

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.checks import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import auth
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect, reverse
from .forms import JoinForm, CustomUserUpdateForm
from mysql.connector import Error
from django.urls import reverse
from .models import CustomUser


def custom_join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            member_data = form.cleaned_data
            if member_data['member_pw'] == member_data['member_repw']:
                # 데이터베이스에 저장
                CustomUser.objects.create(
                    username=member_data['member_id'],
                    password=make_password(member_data['member_pw']),
                    phone=member_data['phone'],
                    member_nm=member_data['member_nm'],
                    email=member_data['email'],
                    regisNum=member_data['regisNum']
                )
                # 가입이 정상적으로 완료되면 로그인 페이지로 리다이렉트
                return redirect(reverse('accounts:login'))

    else:
        # GET 요청일 경우 가입 페이지를 렌더링
        form = JoinForm()

    return render(request, 'accounts/join.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        member_id = request.POST['member_id']
        password = request.POST['password']
        user = authenticate(request, username=member_id, password=password)
        if user is not None and check_password(password, user.password):  # 비밀번호 확인 추가
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'accounts/login.html')


def custom_logout(request):
    logout(request)
    return redirect('/')


from django.contrib.auth.hashers import make_password


@login_required
def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            member_pw = form.cleaned_data.get('member_pw', None)
            member_repw = form.cleaned_data.get('member_repw', None)

            if member_pw == member_repw:
                user.password = make_password(member_pw)
                user.phone = form.cleaned_data['phone']
                user.email = form.cleaned_data['email']
            user.save()

            return redirect('accounts:mypage')
    else:
        form = CustomUserUpdateForm(instance=user)

    return render(request, 'accounts/mypage.html', {'form': form})


def index(request):
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


def login_message_required(args):
    pass
