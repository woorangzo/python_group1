from django.urls import path
from .views import custom_login, custom_logout, custom_join, mypage, relatedStocks, issue, stockRecommend, news, \
    analyze, theme, calc, index

app_name = 'accounts'

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('join/', custom_join, name="join"),
    path('mypage/', mypage, name='mypage'),
    path('relatedStocks/', relatedStocks, name='relatedStocks'),
    path('issue/', issue, name='issue'),
    path('stockRecommend/', stockRecommend, name='stockRecommend'),
    path('news/', news, name='news'),
    path('analyze/', analyze, name='analyze'),
    path('theme/', theme, name='theme'),
    path('calc/', calc, name='calc'),
    path('index/', index, name='index'),

]
