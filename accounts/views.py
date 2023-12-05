import random

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import auth
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect, reverse
from .forms import JoinForm
from mysql.connector import Error
from django.urls import reverse
from .models import CustomUser

# def join(request):
#     if request.method == 'POST':
#         form = JoinForm(request.POST)
#         if form.is_valid():
#             member_data = form.cleaned_data
#             if member_data['member_pw'] == member_data['member_repw']:
#                 try:
#                     # masked_password = '*' * len(member_data['member_pw'])
#                     masked_regisNum = '*' * len(member_data['regisNum'])
#                     masked_password = make_password(member_data['member_pw'])
#
#                     # MySQL connection setup
#                     mydb = mysql.connector.connect(
#                         host="localhost",
#                         user="woorangzo",
#                         passwd="1234",
#                         database="woorangzo"
#                     )
#
#                     # Cursor creation
#                     with mydb.cursor() as mc:
#
#
#                         sql = """
#                             INSERT INTO Member (
#                                 member_id, member_pw, phone, username, email, regisNum,
#                                 created_at, updated_at
#                             ) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
#                         """
#
#                         mc.execute(sql, (
#                             member_data['member_id'],
#                             masked_password,
#                             member_data['phone'],
#                             member_data['username'],
#                             member_data['email'],
#                             masked_regisNum
#
#                         ))
#
#                     mydb.commit()
#                     print("Form data:", member_data)
#                     return redirect('accounts:custom_login')
#
#                 except Error as e:
#                     print("Database Error:", e)
#
#                 finally:
#                     # Close the connection
#                     mydb.close()
#
#     else:
#         form = JoinForm()
#
#     return render(request, 'accounts/join.html', {'form': form})
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
                    realname=member_data['username'],
                    email=member_data['email'],
                    regisNum=member_data['regisNum']
                )
                # 가입이 정상적으로 완료되면 로그인 페이지로 리다이렉트
                return redirect(reverse('accounts:login'))

    else:
        # GET 요청일 경우 가입 페이지를 렌더링
        form = JoinForm()

    return render(request, 'accounts/join.html', {'form': form})

# def login(request):
#     if request.method == "POST":
#         member_id = request.POST['member_id']
#         password = request.POST['password']
#
#         try:
#             # MySQL connection setup
#             mydb = mysql.connector.connect(
#                 host="localhost",
#                 user="woorangzo",
#                 passwd="1234",
#                 database="woorangzo"
#             )
#
#             # Cursor creation
#             with mydb.cursor() as mc:
#                 sql = """
#                     SELECT * FROM Member
#                     WHERE member_id = %s
#                 """
#                 mc.execute(sql, (member_id,))
#                 user_data = mc.fetchone()
#
#                 print("User data from DB:", user_data)  # 디버그 메시지 추가
#
#                 if user_data and check_password(password, user_data[1]):
#                     # Authentication successful
#                     print('Authentication successful')
#                     # 세션에 사용자 정보 저장
#                     request.session['user_data'] = user_data[0]
#                     return redirect('/')
#                 else:
#                     print("Login failed: Username or password is incorrect")
#                     return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect'})
#
#         except Error as e:
#             print("Database Error:", e)
#         finally:
#             # Close the connection
#             mydb.close()
#     else:
#         return render(request, 'accounts/login.html')
def custom_login(request):
    if request.method == 'POST':
        member_id = request.POST['member_id']
        print(member_id)

        password = request.POST['password']
        print(password)
        user = authenticate(request, username=member_id, password=password)
        print(user)
        if user is not None and check_password(password, user.password):  # 비밀번호 확인 추가
            print('Authentication successful. User:', user)  # 디버깅 메시지 추가
            login(request, user)
            return redirect('accounts:index')
        else:
            print('Authentication failed. User:', user)  # 디버깅 메시지 추가
            return render(request, 'accounts/login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'accounts/login.html')



def custom_logout(request):
    logout(request)
    return redirect('accounts:custom_login')



# def logout(request):
#     auth.logout(request)
#     login_url = reverse('accounts:login')  # 'accounts:login'로 수정
#     return redirect(login_url)

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


# def your_view(request):
#     # 기사 목록을 가져오는 코드를 여기에 입력
#     article_list = Article.objects.all().order_by('-published_date') # 최신 기사부터 가져오도록 정렬
#     paginator = Paginator(article_list, 5)  # 페이지 당 5개의 기사를 보여준다.
#
#     page = request.GET.get('page')
#     try:
#         articles = paginator.page(page)
#     except PageNotAnInteger:
#         articles = paginator.page(1)
#     except EmptyPage:
#         articles = paginator.page(paginator.num_pages)
#
#     return render(request, 'news.html', {'articles': articles})










