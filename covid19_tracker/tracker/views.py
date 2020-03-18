from django.template.defaultfilters import date as django_date_filter
from django.http import HttpResponse
from django.shortcuts import render
from . import api
import os
import json
import datetime
from .models import Date


curr_dir = os.getcwd()


def init_db(my_api):
    data = my_api.get_all()
    c = 1
    for country in data:
        print(str(c)+"/159", end='\r', flush=True)
        for date in data[country]:
            conf = data[country][date][0]
            deaths = data[country][date][2]
            recov = data[country][date][1]            
            date = datetime.datetime.strptime(date, '%m/%d/%y')
            d = Date(date=date, confirmed=conf, deaths=deaths, recovered=recov, country=country)
            d.save()
        c+=1


def update_db(my_api):
   # data = my_api.get_today()
   pass


def sum_cases():
    data = Date.objects.filter(date=datetime.date.today())
    if len(data) == 0:
        data = Date.objects.filter(date=datetime.date.today() - datetime.timedelta(days = 1))

    print(len(data))
    inf = 0
    deaths = 0
    reco = 0
    for date in data:
        inf += date.confirmed
        deaths += date.deaths
        reco += date.recovered
    
    return inf, deaths, reco
    

def index(request):
   
    my_api = api.API()

    if Date.objects.count() == 0:
        print("init")
        init_db(my_api)
    else:
        update_db(my_api)

    countries = len(set(Date.objects.all().values_list('country', flat=True)))
    infected, deaths, recovered = sum_cases()
    mortality = (deaths/infected)*100
    return render(request,"index.html",{"infected":infected, "countries":countries, "deaths":deaths, "recovered":recovered, "mortality_rate":round(mortality,2)})
