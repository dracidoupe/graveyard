from unittest import TestCase

from ddcz.html import encode_valid_html, unsafe_encode_valid_creation_html

class TestHtmlRender(TestCase):

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

    # def test_break_variant_2(self):
    #     s = "text that has been &lt;BR/&gt;breaked"
    #     exp = "text that has been <br>breaked"
    #     self.assert_output(s, exp)

    # def test_break_variant_1(self):
    #     s = "text that has been &lt;BR /&gt;breaked"
    #     exp = "text that has been <br>breaked"
    #     self.assert_output(s, exp)



class TestUnsafeHtmlRender(TestCase):

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
        exp = "simple &lt;B onclick=&quot;javascript:script(alert)&quot;&gt;bold</b> text"
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
