from django import template
from app.models import Payroll

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
