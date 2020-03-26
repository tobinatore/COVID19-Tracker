from django import template

register = template.Library()

@register.filter
def percentage(value, arg):
    if arg != 0:
        return round((float(arg)/float(value))*100,2)
    else: return 0

@register.simple_tag
def active(inf, deaths, reco):
    return int(inf)-(int(deaths)+int(reco))

@register.filter
def fix_id(value):
    return value.replace(" ","-")