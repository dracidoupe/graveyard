from django import template

from ..html import encode_valid_html

register = template.Library()

def render_html(value):
    return encode_valid_html(value)

register.filter('render_html', render_html)