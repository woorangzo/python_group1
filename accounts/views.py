import random

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse

from django.views.generic import TemplateView

from accounts.forms import JoinForm

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import JoinForm

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import JoinForm
from .models import Member


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
