from django import template

register = template.Library()

@register.inclusion_tag('carshop/carshop.html')
def show_carshop(request):
    pass
