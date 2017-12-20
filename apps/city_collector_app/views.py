
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
import random
import requests
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    print "im indexing"
    all_cities = City.objects.all()
    context = {
        'all_cities': all_cities,
    }
    return render(request, 'city_collector_app/index.html', context)

def clear(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/city_collector/')

def goHome(request):
    return redirect('/city_collector/')

def process(request):
    print "im processing"
    results = City.objects.form_validator(request.POST)
    if results[0]:
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+request.POST['city']+','+request.POST['country']+'&key=AIzaSyAqDapqiVRbbDY1yMiVJPaJjdSRO6hlvDI').json()
        # search needs to contain component filters for country and locality
        if r['status'] == 'OK':
            print r['results'][0]['address_components']
            print r['results'][0]['geometry']
            city = ''
            country = ''
            for idx in r['results'][0]['address_components']:
                for key, value in idx.iteritems():
                    if key == 'types':
                        for spot in value:
                            if spot == 'country':
                                country = idx['long_name']
                            if spot == 'locality':
                                city = idx['long_name']                    
            lat = r['results'][0]['geometry']['location']['lat']
            lng = r['results'][0]['geometry']['location']['lng']
            print (city,country)
            print (lat,lng)
            if city == '' or country == '':
                if city == '':
                    messages.error(request, 'Your city was not recognized. Try larger city nearby')
                if country == '':
                    messages.error(request, 'Your country spelling was not recognized. Try again please')
            else:
                City.objects.add_city(city, country, lat, lng)
                messages.error(request, 'Your city has been registered! Santa will visit you soon!')
        else:
            messages.error(request, 'We could not find your city on this planet, please try again')
    else:
        for key, error_message in results[1].iteritems():
            messages.error(request, error_message, extra_tags=key)

    return redirect('/city_collector/')