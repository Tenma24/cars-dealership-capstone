import os
import secrets
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError('Set DJANGO_SECRET_KEY in production')
    secret_file = BASE_DIR / '.local-secret'
    if not secret_file.exists():
        secret_file.write_text(secrets.token_urlsafe(64))
    SECRET_KEY = secret_file.read_text().strip()
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver').split(',')
CSRF_TRUSTED_ORIGINS = list(filter(None, os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')))
INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','djangoapp']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','djangoapp.middleware.SecurityHeaders']
ROOT_URLCONF = 'djangoproj.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'frontend/build', BASE_DIR/'frontend/static'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'djangoproj.wsgi.application'
DATABASES = {'default':{'ENGINE':'django.db.backends.sqlite3','NAME':os.getenv('SQLITE_PATH', str(BASE_DIR/'db.sqlite3'))}}
AUTH_PASSWORD_VALIDATORS = [{'NAME':'django.contrib.auth.password_validation.'+name} for name in ['UserAttributeSimilarityValidator','MinimumLengthValidator','CommonPasswordValidator','NumericPasswordValidator']]
LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_TZ=True
STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
STATICFILES_DIRS=[BASE_DIR/'frontend/static']
if (BASE_DIR/'frontend/build/assets').exists():
    STATICFILES_DIRS.append(('assets', BASE_DIR/'frontend/build/assets'))
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Lax'
SESSION_COOKIE_SECURE=not DEBUG
CSRF_COOKIE_SECURE=not DEBUG
SECURE_SSL_REDIRECT=not DEBUG and os.getenv('HTTPS_REDIRECT','1')=='1'
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
SECURE_HSTS_SECONDS=31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
DATA_UPLOAD_MAX_MEMORY_SIZE=65536
BACKEND_URL=os.getenv('BACKEND_URL','http://127.0.0.1:3030').rstrip('/')
SENTIMENT_URL=os.getenv('SENTIMENT_URL','http://127.0.0.1:5050').rstrip('/')
SERVICE_TOKEN=os.getenv('SERVICE_TOKEN','')
