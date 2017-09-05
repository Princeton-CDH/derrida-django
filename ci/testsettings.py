# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = False

# include database settings to use Mariadb ver on production (5.5)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '',
        'TEST': {
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
            },
    },

}

# must be defined for initial setup
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/test-derrida',
        'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores',
    }
}

# for unit tests, that swap test connection in for default
HAYSTACK_TEST_CONNECTIONS = HAYSTACK_CONNECTIONS




# secret key added as a travis build step
