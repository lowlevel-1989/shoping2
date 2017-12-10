from django import template

register = template.Library()

@register.inclusion_tag('shop/cart.html', takes_context=True)
def show_cart_widget(context):
    request = context['request']
    return {'request': request}
