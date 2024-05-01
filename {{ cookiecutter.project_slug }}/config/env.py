from django.core.exceptions import ImproperlyConfigured

import environ

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2

