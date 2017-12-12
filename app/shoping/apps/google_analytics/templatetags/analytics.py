from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('google_analytics/analytics.html')
def analytics(analytics_id=None):

    analytics_id = analytics_id or settings.GOOGLE_ANALYTICS_ID

    return {
        'analytics_id': analytics_id
    }
