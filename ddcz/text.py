import re
from unicodedata import normalize, combining

from django.utils.html import escape


def create_slug(text):
    slug = normalize("NFD", text)
    slug = "".join([ch for ch in slug if not combining(ch)]).lower()
    slug = re.sub("[^a-z0-9]+", "-", slug)
    slug = re.sub("^([^a-z0-9])+", "", slug)
    slug = re.sub("([^a-z0-9]+)$", "", slug)
    return slug


def misencode(text):
    """Take a properly represented text, encode into win1250 and decode
    back into latin2 (iso-8859-2) so it could be encoded back as such over the wire.

    Has to be used when querying database for data stored by original application,
    represented by MisencodedChar/TextField.
    """
    return text.encode("cp1250").decode("latin2")


def escape_user_input(text, newline_to_br=True):
    """
    Escape user input from a text form in a way that's compatible with the v1 version

    Original code:
    function modifystring($string,$wrap=0)
    {
        //$retezec=addslashes($retezec);
        $string=HTMLSpecialChars($string);
        If($zalomit==1):
          $string=eregi_replace("\n","<br />",$string);
        EndIf;

        return $retezec;
    }

    """

    text = escape(text)
    if newline_to_br:
        text = text.replace("\n", "<br />")

    return text
