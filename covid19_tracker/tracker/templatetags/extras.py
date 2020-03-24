from django import template

register = template.Library()

@register.filter
def percentage(value, arg):
    if arg != 0:
        return round((arg/value)*100,2)
    else: return 0

@register.simple_tag
def active(inf, deaths, reco):
    return inf-(deaths+reco)