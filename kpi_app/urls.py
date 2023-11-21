from django.urls import path
from .views import get_kpi_data, get_kosdaq_data

urlpatterns = [
    path('get_kpi_data/', get_kpi_data, name='get_kpi_data'),
    path('get_kosdaq_data/', get_kosdaq_data, name='get_kosdaq_data'),
]