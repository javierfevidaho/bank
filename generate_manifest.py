# generate_manifest.py
import os
import django
from whitenoise.storage import CompressedManifestStaticFilesStorage
from django.conf import settings

# Configurar los ajustes de Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    BASE_DIR=BASE_DIR,
    STATIC_URL='/static/',
    STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles'),
    STATICFILES_DIRS=[
        os.path.join(BASE_DIR, 'core/static'),
    ],
    STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage',
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
        'whitenoise.runserver_nostatic',
    ],
)

django.setup()

# Instanciar CompressedManifestStaticFilesStorage y generar el manifiesto
storage = CompressedManifestStaticFilesStorage()
storage.post_process(None, dry_run=False)
