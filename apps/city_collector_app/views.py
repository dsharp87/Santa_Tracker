
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
import random
import requests
import math
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    print "im indexing"
    all_countries = Country.objects.all()
    all_cities = City.objects.all()
    context = {
        'all_countries': all_countries,
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
    results = Country.objects.entry_validator(request.POST)
    for key, error_message in results[1].iteritems():
        messages.error(request, error_message, extra_tags=key)

    return redirect('/city_collector/')