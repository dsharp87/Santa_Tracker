
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
import random

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

