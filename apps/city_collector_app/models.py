# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime
import requests
# Create your models here.

class CountryManager(models.Manager):
    def entry_validator(self, postData):
        errors = {}
        #validate form input
        if len(postData['city']) < 2:
            errors["city"] = "City name must be at least 2 characters"
        if len(postData['country']) < 2:
            errors["country"] = "Country name must be at least 2 characters"
        if len(errors):
            print "i failed"
            return (False, errors)
        else:
            #validate form input validate google api call
            r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=&components=locality:' + postData['city'] + '|country:' + postData['country'] + '&key=AIzaSyAqDapqiVRbbDY1yMiVJPaJjdSRO6hlvDI').json()
            if not r['status'] == 'OK':
                print "i failed"
                errors['zero_returned'] = 'We could not find your city on this planet, please try again'
                return (False, errors)
            else:
                # print r['results'][0]['address_components']
                # print r['results'][0]['geometry']
                city = ''
                country = ''
                country_code = ''
                for idx in r['results'][0]['address_components']:
                    for key, value in idx.iteritems():
                        if key == 'types':
                            for spot in value:
                                if spot == 'country':
                                    country = idx['long_name']
                                    country_code = idx['short_name']
                                if spot == 'locality':
                                    city = idx['long_name']                    
                lat = r['results'][0]['geometry']['location']['lat']
                lng = r['results'][0]['geometry']['location']['lng']
                print "*"*50
                print (city,country, country_code)
                print (lat,lng)
                print "*"*50
                if city == '' or country == '':
                    if city == '':
                        errors['no_city'] = 'Your city was not recognized. Try larger city nearby'
                    if country == '':
                        errors['no_country'] = 'Your country spelling was not recognized. Try again please'
                if len(errors):
                    print "i failed"
                    return (False, errors)
                else:
                    print "i passed"
                    #check if country is in database
                    if len(Country.objects.filter(name = country)) == 0:
                        s = requests.get('http://api.worldbank.org/v2/countries/'+ country_code + '/indicators/SP.POP.DPND.YG?date=2016:2016&format=json').json()
                        # print s
                        percent_youth = round(s[1][0]['value'])/100
                        print percent_youth
                        t = requests.get('http://api.worldbank.org/v2/countries/'+ country_code + '/indicators/SL.TLF.TOTL.IN?date=2016:2016&format=json').json()
                        # print t
                        total_work_pop = t[1][0]['value']
                        print total_work_pop
                        u = requests.get('http://api.worldbank.org/v2/countries/'+ country_code + '/indicators/SP.POP.TOTL?date=2016:2016&format=json').json()
                        # print u
                        country_pop = u[1][0]['value']
                        print country_pop
                        percent_children = round(float(percent_youth*total_work_pop/country_pop), 2)
                        print percent_children
                        this_country = Country.objects.create(name = country, code = country_code, pop = country_pop, percent_children = percent_children)
                        this_city = City.objects.create(city = city, country = this_country, lat = lat, lng = lng, entry_count = 1)
                        errors['success'] = 'Your city was registered! Santa will be there soon!'
                        return (True, errors)
                    else:
                        if len(City.objects.filter(lat = lat).filter(lng = lng)) > 0:
                            this_city = City.objects.filter(lat = lat).filter(lng = lng)[0]
                            this_city.entry_count += 1
                            this_city.save()
                            errors['success'] = 'Your city was registered! Santa will be there soon!'
                            return (True, errors)
                        else:
                            this_country = Country.objects.filter(name = country)[0]
                            this_city = City.objects.create(city = city, country = this_country, lat = lat, lng = lng, entry_count = 1)
                            errors['success'] = 'Your city was registered! Santa will be there soon!'
                            return (True, errors)
        
class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length = 3)
    pop = models.IntegerField()
    percent_children = models.DecimalField(max_digits=3, decimal_places=2)
    objects = CountryManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class City(models.Model):
    city = models.CharField(max_length=255)
    country = models.ForeignKey(Country, related_name="cities")
    lat = models.FloatField()
    lng = models.FloatField()
    population = models.IntegerField(default = 0)
    entry_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    




#santa actions table