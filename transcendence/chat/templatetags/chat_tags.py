from django import template

register = template.Library()


@register.inclusion_tag('chat/list_button.html')
def list_button(first_name: str = '',
                notification: str = ''):

    return {'name_initial': first_name[:1],
            'first_name': first_name if len(first_name) <= 10 else f"{first_name[:10]}..",
            'notification': notification if len(notification) <= 3 else f"{notification[:3]}..",
            'active': 'd-none' if not notification else ''}

