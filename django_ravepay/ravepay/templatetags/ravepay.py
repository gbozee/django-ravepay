import datetime
from django import template
from django.utils.html import format_html
register = template.Library()


@register.inclusion_tag('rave_button.html', takes_context=True)
def ravepay_button(context, form):
    return {}
