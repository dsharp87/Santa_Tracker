""" Allows looking at list by index when index is a variable in djano templates:
Use as {{ mydict|get_item:item.NAME }} where my dict is an object and item_Name the key of interest}"""
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
