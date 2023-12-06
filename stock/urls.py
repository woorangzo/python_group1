from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('stockRecommend/', views.stock_recommendation_view, name='stockRecommend'),
]
