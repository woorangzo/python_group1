from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('stockRecommend/', views.top_5_stocks, name='top_5_stocks'),
]
