from django.template import Context, Template
from django.test import SimpleTestCase


class TemplateTestCase(SimpleTestCase):
    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)
