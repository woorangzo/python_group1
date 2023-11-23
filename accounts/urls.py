from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import join_user

app_name = 'accounts'

urlpatterns = [
    # Django에서 지원하는 views 라이브러리를 활용 (로그인, 로그아웃, 비밀번호 찾기 & 초기화 등)

    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=False),
         name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('navbar/', auth_views.LoginView.as_view(template_name="accounts/navbar.html", redirect_authenticated_user=False),
         name="navbar"),
    path('', views.mainview),
    path('blank/', views.blank),
    path('mypage/', views.mypage),
    path('relatedStocks/', views.relatedStocks),
    path('issue/', views.issue),
    path('stockRecommend/', views.stockRecommend),
    path('news/', views.news),
    path('analyze/', views.analyze),
    path('theme/', views.theme),
    path('calc/', views.calc),
    path('join/', join_user, name='join'),





]
