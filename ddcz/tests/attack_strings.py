"""
Evil strings that should be used for testing input by users.

Note that all attack should raise a javascript alert, causing the browser to freeze!
If they wouldn't, test suites not intentionally aimed to test a particular evil string
 may end up falsely positive.

All strings should use the _INPUT suffix for an user input and _ESCAPED
for escaped HTML representation. If the escaped representation should be out of HTML/webpage
context, the test suite should introduce its own escaped version.

** Note that in case of Selenium, browser returns the rendered version, hence the
    assert should be against the original _INPUT version **

Courtesy to community of OWASP <https://owasp.org/www-community/xss-filter-evasion-cheatsheet>
<https://owasp.org/www-community/attacks/xss/>
and BLoNS <https://github.com/minimaxir/big-list-of-naughty-strings>
"""

SCRIPT_ALERT_INPUT = "Test <script>alert('Attack')</script>"
SCRIPT_ALERT_ESCAPED = "Test &lt;script&gt;alert('Attack')&lt;/script&gt;"


IMG_TAB_SRC_INPUT = "Test <IMG SRC=\"jav&#x09;ascript:alert('Attack');\">"
IMG_TAB_SRC_ESCAPED = "Test &lt;IMG SRC=\"jav&#x09;ascript:alert('Attack');\"&gt;"
