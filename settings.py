from pathlib import Path
import os

# プロジェクト内でのパスをBASE_DIR / 'subdir' の形式で設定
BASE_DIR = Path(__file__).resolve().parent.parent


# 開発用の設定 - 本番環境には不適切な設定
# 詳細はこちらを参照：https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# セキュリティ警告: 本番環境で使用する秘密鍵は必ず保護すること
SECRET_KEY = 'django-insecure-!!yn=c&557ps!%gygads%0m*^#zu9gx)fhw2+a_b1_!f3n8(dr'

# セキュリティ警告: 本番環境でDEBUGをTrueにしない
DEBUG = False

ALLOWED_HOSTS = ['https://search-project-3bsw.onrender.com', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ocr'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'search_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'search_app.wsgi.application'


# データベース設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQLを使用
        'NAME': os.environ.get('DB_NAME'),          # 環境変数から取得
        'USER': os.environ.get('DB_USER'),          # 環境変数から取得
        'PASSWORD': os.environ.get('DB_PASSWORD'),  # 環境変数から取得
        'HOST': os.environ.get('DB_HOST'),          # 環境変数から取得
        'PORT': '5432',                             # PostgreSQLの標準ポート
    }
}


# パスワード検証設定
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


# 国際化設定
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# 静的ファイル (CSS, JavaScript, 画像) の設定
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 静的ファイルを収集するディレクトリ
STATICFILES_DIRS = [BASE_DIR / "static"],  # 修正

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# デフォルトの主キーのフィールドタイプ
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
