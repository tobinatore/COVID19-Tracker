from django import template

register = template.Library()

@register.filter
def percentage(value, arg):
    if arg != 0:
        return round((arg/value)*100,2)
    else: return 0