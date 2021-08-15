from datetime import timedelta
from django import template

from .. import utils

register = template.Library()


@register.filter(name="rm_second")
def rm_second(td: timedelta):
    def _add_zero(val):
        return "0" + str(val) if val < 10 else str(val)

    try:
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        minutes = _add_zero(minutes)
        return f"{hours}:{minutes}"
    except AttributeError:
        return td


@register.filter(name="lookup")
def lookup(key):
    dict = utils.load_config().item
    return dict[key]
