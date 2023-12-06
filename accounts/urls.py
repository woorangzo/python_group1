
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import join, plot_stock_prices, stock_compare




app_name = 'accounts'

urlpatterns = [
    # Django에서 지원하는 views 라이브러리를 활용 (로그인, 로그아웃, 비밀번호 찾기 & 초기화 등)

    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=False),
         name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('join/', views.join, name="join"),
    path('navbar/', auth_views.LoginView.as_view(template_name="accounts/navbar.html", redirect_authenticated_user=False),
         name="navbar"),
    path('mypage/', views.mypage),
    path('issue/', views.issue),
    path('analyze/', views.analyze),
    path('theme/', views.theme),
    path('calc/', views.calc),
    path('blank/', views.blank),
    path('join/', join, name="join"),
    # path('detail/', views.detail),
    path('', views.mainview, name='mainview'),
    path('plot_stock_prices/', plot_stock_prices, name='plot_stock_prices'),
    path('', views.mainview),
    path('blank/', views.blank),
    path('mypage/', views.mypage),
    path('relatedStocks/', views.relatedStocks),
    path('analyze/', views.analyze),
    path('relatedStocks/', views.relatedStocks, name='relatedStocks'),
    path('stock_compare', stock_compare, name='stock_compare')
]
