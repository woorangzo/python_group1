from django.shortcuts import render, redirect


def mainview(request):
    return render(request, 'accounts/index.html')



