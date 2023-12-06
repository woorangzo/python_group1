from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import stock_compare, update_user, custom_login, custom_logout, custom_join

app_name = 'accounts'

urlpatterns = [
    # Django에서 지원하는 views 라이브러리를 활용 (로그인, 로그아웃, 비밀번호 찾기 & 초기화 등)

    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('join/', custom_join, name="join"),
    path('navbar/',
         auth_views.LoginView.as_view(template_name="accounts/navbar.html", redirect_authenticated_user=False),
         name="navbar"),
    path('mypage/', update_user, name='mypage'),
    path('issue/', views.issue),
    path('analyze/', views.analyze),
    path('theme/', views.theme),
    path('calc/', views.calc),
    path('blank/', views.blank),
    path('blank/', views.blank),
    path('relatedStocks/', views.relatedStocks),
    path('analyze/', views.analyze),
    path('relatedStocks/', views.relatedStocks, name='relatedStocks'),
    path('stock_compare', stock_compare, name='stock_compare')
]
