""" Allows looking at list by index when index is a variable in djano templates:
Use as {{List|index:idx} where idx is for example forloop iterator
{% for idx in range %}
{{List|index:idx}}
{% endfor %}
Can also use as {{List:index:forloop.counter0}}"""

from django import template
register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]
