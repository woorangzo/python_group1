from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.newsList, name='news'),
    path('<str:news_id>', views.news_detail, name='detail')

]
