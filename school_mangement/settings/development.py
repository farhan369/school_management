from school_mangement.settings.common import *
import environ


env = environ.Env()
environ.Env.read_env()
SECRET_KEY = env("SECRET_KEY")

INSTALLED_APPS = [
    # default django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # user defined apps
    "academics",
    "account",
    "event",
    # third party apps
    "rest_framework",
    "rest_framework.authtoken",
]
# To set up authentication using AuthToken
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]

DEBUG = True


# database variables
DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}
