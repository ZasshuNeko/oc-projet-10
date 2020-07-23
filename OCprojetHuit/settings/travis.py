from . import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x693c28g7ptqmwg)enro2wuxe*6-_wovm)d&i90k9-gx#&_4=l'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['35.180.208.255','127.0.0.1']


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
}
