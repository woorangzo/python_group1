import random

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


from django.views.generic import TemplateView


# Create your views here.
def join(request):
    if request.method == "POST":
        username = request.POST['username']

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            # Check if the username is unique
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/join.html', {'error': '이미 존재하는 사용자명입니다.'})

            # Create a new user
            user = User.objects.create_user(username, password=password1)
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/join.html', {'error': '비밀번호가 일치하지 않습니다.'})

    return render(request, 'accounts/join.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
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


def your_view(request):
    # 기사 목록을 가져오는 코드를 여기에 입력
    article_list = Article.objects.all().order_by('-published_date') # 최신 기사부터 가져오도록 정렬
    paginator = Paginator(article_list, 5)  # 페이지 당 5개의 기사를 보여준다.

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {'articles': articles})









