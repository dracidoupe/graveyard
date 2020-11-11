import re
from unicodedata import normalize, combining

def create_slug(text):
    slug = normalize('NFD', text)
    slug = ''.join([ch for ch in slug if not combining(ch)]).lower()
    slug = re.sub("[^a-z0-9]+", "-", slug)
    slug = re.sub("^([^a-z0-9])+", "", slug)
    slug = re.sub("([^a-z0-9]+)$", "", slug)
    return slug

def misencode(text):
    """ Take a properly represented text, encode into win1250 and decode
    back into latin2 (iso-8859-2) so it could be encoded back as such over the wire.

    Has to be used when querying database for data stored by original application,
    represented by MisencodedChar/TextField.
    """
    return text.encode("cp1250").decode("latin2")
    