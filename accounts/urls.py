from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import join, plot_stock_prices, plot_get_stock_prices, plot_industry_stock_prices
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=False),
         name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('join/', join, name="join"),
    path('plot_stock_prices/', plot_stock_prices, name='plot_stock_prices'),
    path('plot_get_stock_prices/', plot_get_stock_prices, name='plot_get_stock_prices'),
    path('plot_industry_stock_prices/', plot_industry_stock_prices, name='plot_industry_stock_prices'),
    path('relatedStocks/', views.relatedStocks),
    path('stockRecommend/', views.stockRecommend),
    path('issue/', views.issue),
    path('navbar/',
         auth_views.LoginView.as_view(template_name="accounts/navbar.html", redirect_authenticated_user=False),
         name="navbar"),
    path('', views.mainview),
    path('blank/', views.blank),
    path('mypage/', views.mypage),
    path('news/', views.news),
    path('analyze/', views.analyze),
    path('theme/', views.theme),
    path('calc/', views.calc),
]
