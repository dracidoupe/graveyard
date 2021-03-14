from django import template

register = template.Library()

@register.filter
def commentTime(datetime):
    return datetime.strftime("%-d. %-m. %Y v %-H:%M:%S")

@register.filter
def commentTimeAlternative(datetime):
    return datetime.strftime("%-H:%M:%S, %-d. %-m. %Y")
