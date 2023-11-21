from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import random

def get_kpi_data(request):
    value = round(random.uniform(2400, 2500), 2)
    change = round(random.uniform(1, 10), 2)
    percent = round((change / value) * 100, 2)

    data = {
        'value': f"{value:.2f}",
        'change': f"▲{change:.2f}",
        'percent': f"+{percent:.2f}%"
    }

    return JsonResponse(data)

def get_kosdaq_data(request):
    value = round(random.uniform(2400, 2500), 2)
    change = round(random.uniform(1, 10), 2)
    percent = round((change / value) * 100, 2)

    data = {
        'value': f"{value:.2f}",
        'change': f"▲{change:.2f}",
        'percent': f"+{percent:.2f}%"
    }

    return JsonResponse(data)