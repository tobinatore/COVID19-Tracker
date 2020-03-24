from django.template.defaultfilters import date as django_date_filter
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import api
import os
import json
import datetime
from .models import Date


curr_dir = os.getcwd()



def get_latest_data():
    data = Date.objects.filter(date=datetime.date.today()).order_by("-confirmed")
    if len(data) == 0:
        data = Date.objects.filter(date=datetime.date.today() - datetime.timedelta(days = 1)).order_by("-confirmed")
        
    return data


def get_all_data():
    return Date.objects.all()


def init_db(my_api):
    data = my_api.get_all()
    c = 1
    for country in data:
        print(str(c)+"\\"+str(len(data)), end='\r', flush=True)
        for date in data[country]:
            conf = data[country][date][0]
            deaths = data[country][date][2]
            recov = data[country][date][1]            
            date = datetime.datetime.strptime(date, '%m/%d/%y')
            d = Date(date=date, confirmed=conf, deaths=deaths, recovered=recov, country=country)
            d.save()
        c+=1


def update_db(my_api):
    c = 1
    data = my_api.get_latest()
    for country in data:
        print(str(c)+"\\"+str(len(data)), end='\r', flush=True)
        for date in data[country]:
            conf = data[country][date][0]
            deaths = data[country][date][2]
            recov = data[country][date][1]            
            date = datetime.datetime.strptime(date, '%m/%d/%y')
            d = Date(date=date, confirmed=conf, deaths=deaths, recovered=recov, country=country)
            d.save()
        c+=1


def sum_cases():
    dates = sorted(set(Date.objects.all().values_list('date', flat=True)))
    conf_sum = []
    death_sum = []
    reco_sum = []
    i = 2
    for date in dates:
        data = Date.objects.filter(date=date)
        inf = 0
        deaths = 0
        reco = 0

        for datapoint in data:
            inf += datapoint.confirmed
            deaths += datapoint.deaths
            reco += datapoint.recovered    
        
        if i % 2 == 0:
            conf_sum.append(inf)
            death_sum.append(deaths)
            reco_sum.append(reco)
        i+=1

    return dates[::2], conf_sum, death_sum, reco_sum


def build_js(dates, conf_sum, death_sum, reco_sum):
    string = "<script> "
    string += "let dates = " + str(dates)+";"
    string += "let conf_sum = " + str(conf_sum)+";"
    string += "let death_sum = " + str(death_sum)+";"
    string += "let reco_sum = " + str(reco_sum)+";"
    string += "</script>"

    return string

def curr_cases(my_api):
    return my_api.get_current_number()    
   
def index(request):
    sum_cases()
    my_api = api.API()

    if Date.objects.count() == 0:
        print("init")
        init_db(my_api)
    elif len(Date.objects.filter(date=datetime.date.today() - datetime.timedelta(days = 1)).order_by("-confirmed")) == 0:
        update_db(my_api)
    

    ret = sum_cases()
    dates, conf_sum, death_sum, reco_sum = ret[0], ret[1], ret[2], ret[3]
    dates = [date.strftime('%d/%m/%y') for date in dates]
    js = build_js(dates, conf_sum, death_sum, reco_sum)
    countries = len(set(Date.objects.all().values_list('country', flat=True)))
    infected, deaths, recovered = curr_cases(my_api)
    mortality = (deaths/infected)*100
    return render(request,"index.html",{"infected":infected, "countries":countries, \
        "deaths":deaths, "recovered":recovered, "mortality_rate":round(mortality,2), \
        "latest":get_latest_data(), "js":js})


def get_country(request):
    country = request.GET.get('country', None)
    data = {
        country:list(Date.objects.filter(country=country).order_by("date").values("date", "confirmed", "deaths", "recovered"))
    }
    return JsonResponse(data, safe=False)