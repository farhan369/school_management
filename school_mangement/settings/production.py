from school_mangement.settings.common import *
import environ


env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")