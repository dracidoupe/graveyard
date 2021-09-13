import os

from .base import *

if os.environ.get("CIRCLECI", False) == "true":
    print("CircleCI environment detected, importing circle settings...")
    from .circle import *


runtime = os.environ.get("ENVIRONMENT", "local")

if runtime == "production":
    from .production import *
elif runtime == "local":
    try:
        from .local import *
    except ImportError:
        pass
else:
    raise ValueError("ENVIRONMENT (if set) should be set to 'production' or 'local'")
