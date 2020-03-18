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
    for country in data:
        for date in data[country]:
            conf = data[country][date][0]
            deaths = data[country][date][2]
            conf = data[country][date][1]
            d = Date(date=date, confirmed=conf, deaths=deaths, recovered=recov, country=country)
            d.save()


def update_db(my_api):
    data = my_api.get_today()
    
    

def index(request):
    my_api = api.API()
    countries = my_api.get_countries()

    if Date.objects.all() == []:
        init_db(my_api)
    else:
        update_db(my_api)

    return render(request,"index.html",{"infected":get_total_infected(os.path.join(curr_dir, "tracker", "json", "country_data.json")), "deaths":16000, "recovered":5000, "mortality_rate":5})
