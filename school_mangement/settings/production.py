from school_mangement.settings.common import *
import environ


env = environ.Env()
environ.Env.read_env()
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["0.0.0.0", "localhost"]

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_NAME"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}
