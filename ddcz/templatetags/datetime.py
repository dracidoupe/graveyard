from datetime import datetime
from math import floor

from django import template

register = template.Library()


@register.filter
def timestamp_to_difference(seconds):
    minutes = floor(seconds / 60)
    hours = floor(seconds / 60 / 60)
    days = floor(seconds / 60 / 60 / 24)

    if seconds < 60:
        return f"{seconds}s"
    elif minutes < 60:
        seconds = seconds - 60 * minutes
        return f"{minutes}m"
    elif hours < 24:
        minutes = minutes - 60 * hours
        seconds = seconds - 60 * minutes - 60 * 60 * hours
        return f"{hours}h {minutes}m"

    hours = hours - 24 * days
    minutes = minutes - 60 * hours - 24 * 60 * days
    seconds = seconds - 60 * minutes - 60 * 60 * hours - 24 * 60 * 60 * days
    return f"{days}d {hours}h {minutes}m"


@register.filter
def timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp)
