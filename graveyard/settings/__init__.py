import os

from .base import *

if os.environ.get("SERVER_CI", False) == "true":
    print("Server CI environment detected, importing circle settings...")
    from .ci_server import *


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
