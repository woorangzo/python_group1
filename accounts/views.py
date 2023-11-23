import random

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import RegistrationForm
from .models import UserProfile


from django.views.generic import TemplateView


# Create your views here.
def join_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']
            UserProfile.objects.create(username=username, phone_number=phone_number, password=password)
            return redirect('accounts:login')  # Change 'login' to the name of your login view
    else:
        form = RegistrationForm()

    return render(request, 'accounts/join.html', {'form': form})


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