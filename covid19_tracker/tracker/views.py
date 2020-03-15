from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Das ist der COVID-19 Tracker Index!")