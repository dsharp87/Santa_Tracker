
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
import random

# Create your views here.


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

