import os
from settings import *

INSTALLED_APPS += [
    'multiple_db',
]

HAYSTACK_SITECONF = 'multiple_db.search_sites'

HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join('tmp', 'test_whoosh_query')
HAYSTACK_INCLUDE_SPELLING = True
HAYSTACK_USE_MULTIPLE_DB = True

DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.sqlite3',
   },
   'db1': {
      'ENGINE': 'django.db.backends.sqlite3',
   },
   'db2': {
      'ENGINE': 'django.db.backends.sqlite3',
   },
}
