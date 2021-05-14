from unittest import TestCase

from django.template import Context, Template

from ddcz.html import (
    encode_valid_html,
    unsafe_encode_valid_creation_html,
    unsafe_encode_any_creation_html,
)


class TestInsecureHtmlRender(TestCase):
    def assert_output(self, entity_string, expected):
        output = unsafe_encode_any_creation_html(entity_string)
        self.assertEqual(expected, output)

    def test_span_table(self):
        s = """&lt;table&gt;
&lt;tr&gt;&lt;th colspan=&quot;5&quot;&gt;Tabulka poznání nestvůry &lt;/th&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;th&gt;známost tvora&lt;/th&gt;&lt;th&gt;pravděpodobnost&lt;/th&gt;&lt;th&gt;použitá vlastnost&lt;/th&gt;&lt;th&gt;připravenost&lt;/th&gt;&lt;th&gt;obvyklost prostředí&lt;/th&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td&gt;zapomenutý&lt;/td&gt;&lt;td&gt;-30%&lt;/td&gt;&lt;td rowspan=&quot;6&quot;&gt;úroveň + INT%&lt;/td&gt;&lt;td rowspan=&quot;6&quot;&gt;Postava se může připravit, dopředu se seznámit s tvory, které jsou pro daný kraj typičtí atd. Za toto získává bonus +10%&lt;/td&gt;&lt;td rowspan=&quot;6&quot;&gt;Pokud se tvor nachází ve svém obvyklém prostředí, má učenec větší šanci si ho vybavit a naopak. Postava má bonus či postih 10%.&lt;/td&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td&gt;téměř neznámý&lt;/td&gt;&lt;td&gt;0%&lt;/td&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td&gt;neobvyklý&lt;/td&gt;&lt;td&gt;15%&lt;/td&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td&gt;běžný&lt;/td&gt;&lt;td&gt;30%&lt;/td&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td&gt;velmi známý&lt;/td&gt;&lt;td&gt;45%&lt;/td&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td&gt;slavný&lt;/td&gt;&lt;td&gt;60%&lt;/td&gt;&lt;/tr&gt;
&lt;/table&gt;"""

        exp = """<table>
<tr><th colspan="5">Tabulka poznání nestvůry </th></tr>
<tr><th>známost tvora</th><th>pravděpodobnost</th><th>použitá vlastnost</th><th>připravenost</th><th>obvyklost prostředí</th></tr>
<tr><td>zapomenutý</td><td>-30%</td><td rowspan="6">úroveň + INT%</td><td rowspan="6">Postava se může připravit, dopředu se seznámit s tvory, které jsou pro daný kraj typičtí atd. Za toto získává bonus +10%</td><td rowspan="6">Pokud se tvor nachází ve svém obvyklém prostředí, má učenec větší šanci si ho vybavit a naopak. Postava má bonus či postih 10%.</td></tr>
<tr><td>téměř neznámý</td><td>0%</td></tr>
<tr><td>neobvyklý</td><td>15%</td></tr>
<tr><td>běžný</td><td>30%</td></tr>
<tr><td>velmi známý</td><td>45%</td></tr>
<tr><td>slavný</td><td>60%</td></tr>
</table>"""
        self.assert_output(s, exp)


class TestUnsafeHtmlRenderTemplate(TestCase):
    def assert_output(self, entity_string, expected, template_str):
        template = Template(template_str)
        output = template.render(Context({"entity_string": entity_string}))
        self.assertEqual(expected, output)

    def test_easy_template(self):
        entity_string = "&lt;h2&gt;&lt;a&gt;Mnich&lt;/a&gt;&lt;/h2&gt;"
        exp = "<h2><a>Mnich</a></h2>"
        t = "{% load html %}{{ entity_string|render_html_insecurely|safe }}"
        self.assert_output(entity_string, exp, t)


class TestUserHtmlRender(TestCase):
    def assert_output(self, entity_string, expected):
        output = encode_valid_html(entity_string)
        self.assertEqual(expected, output)

    def test_text_returned(self):
        s = "Simple plain text"
        self.assert_output(s, s)

    def test_pair_tag_uppercase_accepted(self):
        s = "simple &lt;B&gt;bold&lt;/B&gt; text"
        exp = "simple <b>bold</b> text"
        self.assert_output(s, exp)

    def test_par_tag_lowercase_accepted(self):
        s = "simple &lt;b&gt;bold&lt;/b&gt; text"
        exp = "simple <b>bold</b> text"
        self.assert_output(s, exp)

    def test_attributes_unsupported(self):
        s = "simple &lt;B onclick=&quot;javascript:script(alert)&quot;&gt;bold&lt;/B&gt; text"
        exp = "simple &lt;B onclick=&quot;javascript:script(alert)&quot;&gt;bold&lt;/B&gt; text"
        self.assert_output(s, exp)

    def test_nonpair_accepted(self):
        s = "simple &lt;HR&gt; line"
        exp = "simple <hr> line"
        self.assert_output(s, exp)

    def test_break_variant_3(self):
        s = "text that has been &lt;BR&gt;breaked"
        exp = "text that has been <br>breaked"
        self.assert_output(s, exp)

    def test_break_variant_2(self):
        s = "text that has been &lt;BR/&gt;breaked"
        exp = "text that has been <br>breaked"
        self.assert_output(s, exp)

    def test_break_variant_1(self):
        s = "text that has been &lt;BR /&gt;breaked"
        exp = "text that has been <br>breaked"
        self.assert_output(s, exp)

    def test_bad_trailing_arrow(self):
        s = "&lt;h2&gt;Skřetí zabijáci&lt;/h2&gt;&lt;"
        exp = "<h2>Skřetí zabijáci</h2>&lt;"
        self.assert_output(s, exp)


class TestDeprecatedUnsafeHtmlRender(TestCase):
    def assert_output(self, entity_string, expected):
        output = unsafe_encode_valid_creation_html(entity_string)
        self.assertEqual(expected, output)

    def test_text_returned(self):
        s = "Simple plain text"
        self.assert_output(s, s)

    def test_pair_tag_uppercase_accepted(self):
        s = "simple &lt;B&gt;bold&lt;/B&gt; text"
        exp = "simple <b>bold</b> text"
        self.assert_output(s, exp)

    def test_par_tag_lowercase_accepted(self):
        s = "simple &lt;b&gt;bold&lt;/b&gt; text"
        exp = "simple <b>bold</b> text"
        self.assert_output(s, exp)

    def test_attributes_unsupported_without_pair_check(self):
        s = "simple &lt;B onclick=&quot;javascript:script(alert)&quot;&gt;bold&lt;/B&gt; text"
        exp = (
            "simple &lt;B onclick=&quot;javascript:script(alert)&quot;&gt;bold</b> text"
        )
        self.assert_output(s, exp)

    def test_nonpair_accepted(self):
        s = "simple &lt;HR&gt; line"
        exp = "simple <hr> line"
        self.assert_output(s, exp)

    def test_break_variant_3(self):
        s = "text that has been &lt;BR&gt;breaked"
        exp = "text that has been <br>breaked"
        self.assert_output(s, exp)

    def test_break_variant_2(self):
        s = "text that has been &lt;BR/&gt;breaked"
        exp = "text that has been <br>breaked"
        self.assert_output(s, exp)

    def test_break_variant_1(self):
        s = "text that has been &lt;BR /&gt;breaked"
        exp = "text that has been <br>breaked"
        self.assert_output(s, exp)

    def test_empty_link(self):
        s = "text with &lt;a&gt;empty link&lt;/a&gt;"
        exp = "text with <a>empty link</a>"
        self.assert_output(s, exp)

    def test_empty_link_in_heading(self):
        s = "&lt;h2&gt;&lt;a&gt;Mnich&lt;/a&gt;&lt;/h2&gt;"
        exp = "<h2><a>Mnich</a></h2>"
        self.assert_output(s, exp)
