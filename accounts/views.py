import random

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import  check_password
from django.contrib import auth
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect
from .forms import JoinForm
from mysql.connector import Error

def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            member_data = form.cleaned_data
            if member_data['member_pw'] == member_data['member_repw']:
                try:
                    masked_password = '*' * len(member_data['member_pw'])
                    masked_regisNum = '*' * len(member_data['regisNum'])

                    # MySQL connection setup
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="woorangzo",
                        passwd="1234",
                        database="woorangzo"
                    )

                    # Cursor creation
                    with mydb.cursor() as mc:


                        sql = """
                            INSERT INTO Member (
                                member_id, member_pw, phone, username, email, regisNum,
                                created_at, updated_at
                            ) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """

                        mc.execute(sql, (
                            member_data['member_id'],
                            masked_password,
                            member_data['phone'],
                            member_data['username'],
                            member_data['email'],
                            masked_regisNum

                        ))

                    mydb.commit()
                    print("Form data:", member_data)
                    return redirect('accounts:login')

                except Error as e:
                    print("Database Error:", e)

                finally:
                    # Close the connection
                    mydb.close()

    else:
        form = JoinForm()

    return render(request, 'accounts/join.html', {'form': form})


def login(request):
    if request.method == "POST":
        member_id = request.POST['member_id']
        password = request.POST['password']

        try:
            # MySQL connection setup
            mydb = mysql.connector.connect(
                host="localhost",
                user="woorangzo",
                passwd="1234",
                database="woorangzo"
            )

            # Cursor creation
            with mydb.cursor() as mc:
                sql = """
                    SELECT * FROM Member
                    WHERE member_id = %s
                """
                mc.execute(sql, (member_id,))
                user_data = mc.fetchone()

                if user_data and check_password(password, user_data['member_pw']):
                    # Authentication successful
                    return redirect('singlepage:index')
                else:
                    return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect'})

        except Error as e:
            print("Database Error:", e)
        finally:
            # Close the connection
            mydb.close()
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('index')
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









