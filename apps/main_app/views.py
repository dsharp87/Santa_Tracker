
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
import random
from tsp import optimized_santa_route
from ..city_collector_app.models import City, Country

# Create your views here.
'''
Notes on APIs:
World Bank API call for % of population that are dependent minors
http://api.worldbank.org/v2/countries/all/indicators/SP.POP.DPND.YG?date=2016:2016 XML format
http://api.worldbank.org/v2/countries/all/indicators/SP.POP.DPND.YG?format=json JSON format <- Messy gives all the years

https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structure
https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-api-indicator-queries

https://maps.googleapis.com/maps/api/directions/json?origin=Adelaide,SA&destination=Adelaide,SA&waypoints=optimize:true|Barossa+Valley,SA|Clare,SA|Connawarra,SA|McLaren+Vale,SA&key=API_KEY


'''
def routegen(request):
    #create dictionary that will be passed to optimized santa_route
    route_cities = {
        'city_names' : [],
        'city_coords' : [],
        'start_city' : request.session['start_city']
    }
    #get all cities from database, and add them to dictionary
    cities = City.objects.all()
    for city in cities:
        route_cities['city_names'].append(city.city)
        route_cities['city_coords'].append([city.lat, city.lng])
    
    #call optimize tsp file on our city list
    route_results = optimized_santa_route(route_cities)
    time_per_present = 0.001

    # this reads the travel plan and calculates num of presents and time to diliver them all
    # this won't function until we are able to get city pop, and then utilize results in mapping view
    for city in route_results['travel_plan']:
        city_obj = City.objects.get(city=city.name)
        city_pop = city_obj.population
        youth_percent = city_obj.country.youth_percent
        city_present_count = city_pop * youth_percent
        city['time']  =  time_per_present * city_present_count
        city['present_count'] = int(city_present_count)
    
    #passes our dictionary from tsp 
    # results = {
    #     'miles_traveled': 0,
    #     'travel_plan':[{name:city_name, coords:[xx.xxx, xx.xxxx]}, {name:city_name, coords:[xx.xxx, xx.xxxx]}, {name:city_name, coords:[xx.xxx, xx.xxxx]}],
    # }
    # this is returned back to optimized_santa_route (miles travled and travel plan list of dictionaries)
    return render(request, 'main_app/travel.html',route_results)


def index(request):
    context = {
        "key":"value"
    }
    return render(request, 'main_app/index.html', context)

def clear(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

def goHome(request):
    return redirect('/')

