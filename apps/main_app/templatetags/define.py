from django import template
register = template.Library()

""" Allows to assign value to variable in django template.
it used in this way:

{% if item %}

   {% define "Edit" as action %}

{% else %}

   {% define "Create" as action %}

{% endif %}

Would you like to {{action}} this item
"""

@register.assignment_tag
def define(val=None):
  return val
