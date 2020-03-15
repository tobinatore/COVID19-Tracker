from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,"index.html",{"infected":140000, "deaths":16000, "recovered":5000, "mortality_rate":5})