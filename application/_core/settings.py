import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv as env_load

# Load environment variables
env_load()

# Mar - using the .env file
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = get_random_secret_key()
DB_URL = os.getenv("DATABASE_URL", "default_db_url")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# separate the hosts with a space
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(" ")

# Open the settings.py file and look for the INSTALLED_APPS list
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "application.main",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# mar - custom
ROOT_URLCONF = "application._core.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "application._core.wsgi.application"


# mar - custom
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "_core/database/db.sqlite3",
    }
    # Mar: dj-database-url for Render PG, it is installed to convert the database url to the django config above
    # "default": dj_database_url.parse(DB_URL)
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Mar: Custom Static File Area for CSS & JS
STATIC_URL = "application/static/"
STATIC_ROOT = BASE_DIR.parent / "static"

# for local static files locator for each application created
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

if DEBUG == "False":
    # Mar: HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Mar: HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 Year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
    SESSION_SAVE_EVERY_REQUEST = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# for tailwind css local [for use of the python manage.py collectstatic]
# in production, we need a cdn files (contents delivery network)
# STATIC_ROOT = BASE_DIR.parent / "production-cdn" / "static"

# Mar: for whitenoise storage, solved the js problem
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Mar: DataFlair for Local Memory Cache (do not change)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "DataFlair",
    }
}
