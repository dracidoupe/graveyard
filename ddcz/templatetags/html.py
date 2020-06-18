from django import template

from ..html import encode_valid_html, unsafe_encode_valid_creation_html

register = template.Library()

def render_html(value):
    return encode_valid_html(value)

register.filter('render_html', render_html)

def render_html_insecurely(value):
    return unsafe_encode_valid_creation_html(value)

register.filter('render_html_insecurely', render_html)
