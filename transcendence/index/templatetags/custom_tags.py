from django import template
from django.urls import reverse

register = template.Library()


# @register.inclusion_tag('frontend/game/game_menu.html')
# def render_game_menu(title, game, play_link, lobby_link, *args, **kwargs):
#     return {
#         'title': title,
#         'game': game,
#         'play_link': play_link,
#         'lobby_link': lobby_link
#     }


@register.inclusion_tag('index/card_big.html')
def card_big(title):
    return {
        'title': title
    }


@register.inclusion_tag('index/card_small.html')
def card_small(title):
    return {
        'title': title
    }