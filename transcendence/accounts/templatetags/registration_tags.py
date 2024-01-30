from django import template
from widget_tweaks.templatetags.widget_tweaks import render_field as wt_render_field

register = template.Library()


@register.inclusion_tag('accounts/registration_helpers/base_field.html')
def render_form_field(form, field_name, css_class=""):
    field = form[field_name]
    return {'field': field, 'css_class': f'form-control {css_class}', 'placeholder': f'{str.capitalize(field_name)}'}


@register.inclusion_tag('accounts/registration_helpers/password_field.html')
def render_pass_field(form, field_name, css_class="", placeholder=""):
    field = form[field_name]
    return {'field': field, 'css_class': f'form-control {css_class}', 'placeholder': f'{placeholder}'}
