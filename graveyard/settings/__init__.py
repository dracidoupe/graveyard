import os

from .base import *

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
