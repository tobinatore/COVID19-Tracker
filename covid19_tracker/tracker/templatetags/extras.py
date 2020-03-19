from django import template

register = template.Library()

@register.filter
def percentage(value, arg):
    return round((arg/value)*100,2)