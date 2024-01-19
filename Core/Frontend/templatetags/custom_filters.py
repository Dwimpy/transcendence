from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def dynamic_url(view_name, *args):
    return reverse(view_name, None, args)