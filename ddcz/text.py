import re
from unicodedata import normalize, combining

def create_slug(text):
    slug = normalize('NFD', text)
    slug = ''.join([ch for ch in slug if not combining(ch)]).lower()
    slug = re.sub("[^a-z0-9]+", "-", slug)
    slug = re.sub("^([^a-z0-9])+", "", slug)
    slug = re.sub("([^a-z0-9]+)$", "", slug)
    return slug
