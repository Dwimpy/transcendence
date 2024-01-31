from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag('accounts/base_templates/base_field.html')
def render_base_field(form, field_name, css_class=""):
    field = form[field_name]
    return {'field': field, 'css_class': f'form-control {css_class}', 'placeholder': f'{str.capitalize(field_name)}'}


@register.inclusion_tag('accounts/base_templates/password_field.html')
def render_pass_field(form, field_name, css_class="", placeholder=""):
    field = form[field_name]
    return {'field': field, 'css_class': f'form-control {css_class}', 'placeholder': f'{placeholder}'}


@register.inclusion_tag('accounts/base_templates/base_form.html')
def render_base_form(title, form, path, url):
    return {'title': title, 'form': form, 'url': reverse_lazy(url), 'content_path': path}


@register.inclusion_tag('accounts/base_templates/base_form.html')
def render_profile_form(title, form, user, path, url_name, logged_user):
    url = reverse_lazy(url_name, args=[user.username])
    return {'title': title, 'form': form, 'user': user, 'url': url, 'content_path': path, 'logged_user': logged_user}