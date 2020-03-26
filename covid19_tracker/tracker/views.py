from django.template.defaultfilters import date as django_date_filter
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import api
import os
import json
import datetime
from .models import Date, Live


curr_dir = os.getcwd()


def fetch_live(my_api):
    data = my_api.get_live()

    for country in data:
        live = Live(time=datetime.datetime.now()+datetime.timedelta(hours=1), confirmed=country.confirmed, deaths=country.deaths, \
                active=country.active, new_cases=country.new_cases, new_deaths=country.new_deaths, country=country.country,\
                serious=country.serious, mortality=country.mortality, recovered=country.recovered)
        live.save()


def update_live(my_api):
    data = Live.objects.all()
    data.delete()

    data_new = my_api.get_live()
    for country in data:
        live = Live(time=datetime.datetime.now().strftime("%H:%M:%S"), confirmed=country.confirmed, deaths=country.deaths, \
                active=country.active, new_cases=country.new_cases, new_deaths=country.new_deaths, country=country.country,\
                serious=country.serious, mortality=country.mortality, recovered=country.recovered)
        live.save()


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
            deaths = data[country][date][1]
            #recov = data[country][date][1]            
            date = datetime.datetime.strptime(date, '%m/%d/%y')
            d = Date(date=date, confirmed=conf, deaths=deaths, recovered=0, country=country)
            d.save()
        c+=1


def update_db(my_api):
    c = 1
    data = my_api.get_latest()
    for country in data:
        print(str(c)+"\\"+str(len(data)), end='\r', flush=True)
        for date in data[country]:
            conf = data[country][date][0]
            deaths = data[country][date][1]
            #recov = data[country][date][1]            
            date = datetime.datetime.strptime(date, '%m/%d/%y')
            d = Date(date=date, confirmed=conf, deaths=deaths, recovered=0, country=country)
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
            reco_sum.append(0)
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
    
    if Live.objects.count() == 0:
        fetch_live(my_api)
    elif Live.objects.filter(country="Global")[0].time < datetime.datetime.now().time():
        update_live(my_api)

    ret = sum_cases()
    dates, conf_sum, death_sum, reco_sum = ret[0], ret[1], ret[2], ret[3]
    dates = [date.strftime('%d/%m/%y') for date in dates]
    
    js = build_js(dates, conf_sum, death_sum, reco_sum)
    
    country_list = sorted(set(Date.objects.all().values_list('country', flat=True)))
    countries = len(country_list)
    
    global_ = Live.objects.filter(country="Global")
    confirmed = global_[0].confirmed
    deaths = global_[0].deaths
    reco = global_[0].recovered
    mortality = (deaths/confirmed)*100

    print()
    
    return render(request,"index.html",{"infected":confirmed, "countries":countries, \
        "deaths":deaths, "recovered":reco, "mortality_rate":round(mortality,2), \
        "latest":Live.objects.all().order_by("-confirmed")[1:], "js":js, "country_list":country_list})


def get_country(request):
    country = request.GET.get('country', None)    
    data = {
        country:list(Date.objects.filter(country=country).order_by("date").values("date", "confirmed", "deaths", "recovered"))
    }
    return JsonResponse(data, safe=False)