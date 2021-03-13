from django import template

register = template.Library()

@register.filter(name='articleTime')
def articleTime(datetime):
    return datetime.strftime("%-d. %-m. %Y v %-H:%M")

@register.filter(name='commentTime')
def commentTime(datetime):
    return datetime.strftime("%-d. %-m. %Y v %-H:%M:%S")

@register.filter(name='articleTimeAlternative')
def articleTimeAlternative(datetime):
    return datetime.strftime("%-H:%M, %-d. %-m. %Y")

@register.filter(name='commentTimeAlternative')
def commentTimeAlternative(datetime):
    return datetime.strftime("%-H:%M:%S, %-d. %-m. %Y")
