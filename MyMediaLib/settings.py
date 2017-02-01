"""
Django settings for MyMediaLib project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




'''Settings for MyMediaLib project'''

import logging, logging.config
import re


'''
MEDIA_LIB is a folder with media files. Nothing more.

Structure
1. Could include any folders with any files, it wouldn't
affect library processing. So you can keep any folder
structure you like. MML will never move your files inside library.
I bet you already have a folder with your photos and videos. You can
point MEDIA_LIB to that folder and it will work. Nothing will change
inside your folder.
2. You can add new files to MEDIA_LIB folder manually and run import
from MEDIA_LIB. MML will scan it and new files would be available from
web interface.
3. MML will use AUTOIMPORT_PATH to store automatically imported
files. It will make AUTOIMPORT/yyyy/mm/dd/ folders structure and use it
to store automatically imported media files (those with date). Automatically
imported media files which do not have date inside, will go to
AUTOIMPORT/import_yyyy_mm_dd folder. Also MML will try to guess file date
based on its name when possible.
'''
# MEDIA_LIB = u'/var/raid/Media/Photo'
MEDIA_LIB = '/var/raid/Projects/MyMediaLib/test_files/test_lib'


'''
A list of locations where to look for new files.
'''
IMPORT_FROM = [
    u'/var/raid/Projects/MyMediaLib/test_files/test_import'
    # u'/var/media/iPhone',
]

'''
AUTOIMPORT_PATH - Path to store media files imported from directories
other then MEDIA_LIB. If file being importing from MEDIA_LIB - it will
stay on its place. So user can make his own structure of folders inside
MEDIA_LIB. When files come from other places, MML will put it into
YEAR/MONTH/DAY folder structure inside AUTOIMPORT_PATH.
'''
AUTOIMPORT_PATH = os.path.join(MEDIA_LIB, 'autoimport')


'''
MML_PATH is where system related things are stored.
'''
MML_PATH = os.path.join(MEDIA_LIB, '_mml')

'''
Path to store generated thumbs. No need to back it up.
You're making backups, aren't you??
'''
CACHE_PATH = os.path.join(MML_PATH, 'cache')

'''
MML will iterate over extensions and decide which parser to use.
Extensions are lower case. File parsers are valid class names.
'''
FILE_PARSERS = {
    'files.models.PhotoFile': ('.jpg', 'thm'),
    'files.models.RawPhoto': ('.cr2', ),
    'files.models.VideoFile': ('.mp4', '.mov', 'lrv')
}

'''
MML wouldn'd import files which match any of IGNORE_FILE_PATTERNS
'''
IGNORE_FILE_PATTERNS = (
    re.compile('^(\._)?\.DS_Store$', flags=re.IGNORECASE),
    re.compile('^\..*', flags=re.IGNORECASE)
)

THUMB_SIZE = (128, 128)
PREVIEW_SIZE = (2560, 1600)

# dcraw executable to read various raw photo format
DCRAW_EXE = os.path.join(BASE_DIR, 'util/dcraw/dcraw')
EXIFTOOL_PATH = os.path.join(BASE_DIR, 'util/Image-ExifTool-10.33/exiftool')






TIME_ZONE = 'Europe/Moscow'

POPOVER_API_TOKEN = 'a2rwdq2rv959nh7zd1g1zye8qm6qor'
POPOVER_USER_KEY = 'ug5af83ry7g53m8pba52hokfqrs7xk'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
        },
        'simple_console': {
            'format': '%(message)s'
        },
        'email': {
            'format': '%(message)s\n\n%(asctime)s %(levelname)s %(name)s'
        },
        'push_notification':{
            'format': '%(message)s\n%(levelname)s %(name)s'
        }
    },
    'handlers': {
        # 'null': {
        #     'level':'DEBUG',
        #     'class':'django.utils.log.NullHandler',
        # },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple_console'
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'filters': ['special']
        # }

        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/nas/MyMediaLib.log',
            'maxBytes': 10000,
            'backupCount': 5,
            'formatter': 'simple'
        },
        'email': {
            'level': 'WARNING',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': ('192.168.1.3', 25),
            'fromaddr': 'admin@suhenky.com',
            'toaddrs': ['serafim@suhenky.com'],
            'subject': 'MyMediaLib log',
            'credentials': ('admin', 'outrun96#tints'),
            'secure': (),
            'formatter': 'email'
        },
        'push_notification': {
            'level': 'INFO',
            'class': 'util.logging_handlers.PushoverHandler',
            'formatter': 'push_notification',
            'api_token': POPOVER_API_TOKEN,
            'user_key': POPOVER_USER_KEY
        }
    },
    'loggers': {
        'django': {
            # 'handlers':['console', 'file', 'email', 'push_notification'],
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'files': {
            # 'handlers':['console', 'file', 'email', 'push_notification'],
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'devices': {
            # 'handlers':['console', 'file', 'email', 'push_notification'],
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        # 'nas.find-torrents': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
        # 'myproject.custom': {
        #     'handlers': ['console', 'mail_admins'],
        #     'level': 'INFO',
        #     'filters': ['special']
        # }
    }
}



############### Django settings ######################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0s=lv82etp%%u60&y_5t#83&uuw+oni=^%uwkdsm!g(2likz_1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'files',
    'devices',
    'web'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyMediaLib.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MyMediaLib.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MML_PATH, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'



USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_LIB