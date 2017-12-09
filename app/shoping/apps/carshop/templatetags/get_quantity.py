from django import template

register = template.Library()

@register.filter
def get_quantity(pk, obj):
    return obj[str(pk)]
