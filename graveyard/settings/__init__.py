import os

from .base import *

if 'CIRCLECI' in os.environ and os.environ['CIRCLECI'] == "true":
    print('CircleCI environment detected, importing circle settings...')
    from .circle import *

try:
    from .production import *
except ImportError:
    try:
        from .local import *
    except ImportError:
        pass

