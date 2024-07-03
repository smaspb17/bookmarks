import os

from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_extensions',
    'social_django',
    'easy_thumbnails',
    'images.apps.ImagesConfig',
    'actions.apps.ActionsConfig',
    'debug_toolbar',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2',

]

ROOT_URLCONF = "bookmarks.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "bookmarks.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
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

LANGUAGE_CODE = "ru-Ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# редиректы аутентификации
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# использование электронной почты (мнимое - через консоль)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Для информации - стандартный список хешеров паролей.
# Для хеширования применяется 1-ый
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

# конвейер соц аутентификации
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    # 'social_core.pipeline.social_auth.social_user',
    'account.pipeline.social_user',
    'social_core.pipeline.user.get_username',
    # 'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    'account.pipeline.new_users_handler',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# OAuth2.0 in GitHub
SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')

# OAuth2.0 in VK
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

# OAuth2.0 in Twitter
SOCIAL_AUTH_TWITTER_KEY = os.getenv('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.getenv('SOCIAL_AUTH_TWITTER_SECRET')

# OAuth2.0 in Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


# Альтернативный параметр для указания URL-адреса модели (в т.ч. User) -
# динамически добавляет в указанные модели метод get_absolute_url()
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail',
                                        args=[u.username])
}

# REDIS
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
