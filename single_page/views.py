import random

from django.http import JsonResponse
from django.shortcuts import render


def mainview(request):
    return render(request, 'accounts/index.html')


