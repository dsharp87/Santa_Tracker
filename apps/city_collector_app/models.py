# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime
# Create your models here.

class CityManager(models.Manager):
    def form_validator(self, postData):
        errors = {}
        if len(postData['city']) < 2:
            errors["city"] = "City name must be at least 2 characters"
        if len(postData['country']) < 2:
            errors["country"] = "Country name must be at least 2 characters"
        if len(errors):
            print "i failed"
            return (False, errors)
        else:
            print "i passed"
            return (True, "yay")

    def add_city(self, city, country, lat, lng):
        print len(City.objects.filter(lat = lat).filter(lng = lng))
        if len(City.objects.filter(lat = lat).filter(lng = lng)) > 0:
            this_city = City.objects.filter(lat = lat).filter(lng = lng)[0]
            this_city.entry_count += 1
            this_city.save()
            print this_city.entry_count
            return this_city
        else:
            this_city = City.objects.create(city = city, country = country, lat = lat, lng = lng, entry_count = 1)
            print this_city.city
            return this_city
        


class City(models.Model):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255) # country needs to be its own class/table
    lat = models.FloatField()
    lng = models.FloatField()
    population = models.IntegerField(default = 0)
    percent_children = models.FloatField(default = 0)
    entry_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CityManager()


#santa actions table