from .base import *  # noqa: F403

DEBUG = True


INSTALLED_APPS.extend(  # noqa: F405
    [
        "debug_toolbar",
        "django_extensions",
    ]
)
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

INTERNAL_IPS = ("127.0.0.1",)

MEDIA_URL = "http://127.0.0.1:8000/media/"
