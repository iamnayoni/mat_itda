from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_spoons(score):
    filled = '<i class="bi bi-star-fill spoon-filled"></i>'
    empty = '<i class="bi bi-star spoon-empty"></i>'
    try:
        score = int(score)
    except (TypeError, ValueError):
        score = 0
    score = max(0, min(5, score))
    return mark_safe((filled * score) + (empty * (5 - score)))


@register.filter
def in_list(value, lst):
    return value in lst
