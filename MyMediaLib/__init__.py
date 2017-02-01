from util import mkdir_p
from django.conf import settings


# Ensure we have all directories from settings
mkdir_p(settings.MEDIA_LIB)
mkdir_p(settings.AUTOIMPORT_PATH)
mkdir_p(settings.MML_PATH)
mkdir_p(settings.CACHE_PATH)
