"""
Django settings for flower_shop project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import sys
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# sys.path.insert(0, str(Path(BASE_DIR,'flower_shop/apps')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4*dvaqhgbh9t+d97tzj66%aij7*ravbh!uek!dg#ok@hdcc=_b'

# Application definition
INSTALLED_APPS = [
    # 'simpleui',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'contents',
    'verifications',
    'areas',
    'goods',
    'carts',
    'orders',
    'payments'
]
sys.path.insert(0, str(BASE_DIR / 'flower_shop/apps'))
# print(str(BASE_DIR / 'flower_shop/apps'))
ROOT_URLCONF = 'flower_shop.urls'
# 指定自定义的用户模型类：值的语法 ==> '子应用.用户模型类'
AUTH_USER_MODEL = 'users.User'
# 指定自定义用户认证后端
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileBackend']
# 判断用户是否登录后，指定未登录用户重定向的地址
LOGIN_URL = '/login/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'flower_shop/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'environment': 'flower_shop.utils.jinja2_env.jinja2_environment',
        },
    },{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'flower_shop/templates'],
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
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
WSGI_APPLICATION = 'flower_shop.wsgi.application'
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# 指定默认的邮费
FREIGHT = 80
CACHES = {
    "default": { # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": { # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": { # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 浏览记录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 购物车
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_DEPRECATED_PYTZ=True
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'flower_shop/static',
    ]
# STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = BASE_DIR / 'static/'

# 配置静态文件加载路径
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 支付宝配置
ALIPAY_APPID = '2021000119640437'  # appid
ALIPAY_DEBUG = True  # 设置为True表示使用沙箱，设置为False则为正式环境
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'  # 支付网关，固定
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/payment/status/'  # 支付成功后，支付宝返回的地址

# DEBUG = False
ALLOWED_HOSTS = []
DEBUG = True
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR/'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql', # 数据库引擎
        'HOST': '127.0.0.1', # 数据库主机
        'PORT': 3306, # 数据库端口
        'USER': 'root', # 数据库用户名
        'PASSWORD': 'Password123.', # 数据库用户密码
        'NAME': 'flower' # 数据库名字
    }
}
# simpleui 配置
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
# 隐藏首页的快捷操作和最近动作
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_LOGIN_PARTICLES = False  # 是否关闭粒子动画
# 修改左侧菜单首页设置
SIMPLEUI_HOME_PAGE = '/dashboard/1/'
SIMPLEUI_HOME_TITLE = '数据中台'  # 首页标题
# 修改首页设置, 指向新创建的控制面板
SIMPLEUI_DEFAULT_THEME = 'element.css'  # 主题修改
# 设置右上角Home图标跳转链接，会以另外一个窗口打开
SIMPLEUI_INDEX = 'http://127.0.0.1:8000'
# SIMPLEUI_HOME_ICON = 'fa fa-user'   # 首页图标
SIMPLEUI_LOGO = 'http://127.0.0.1:8000/static/imgs/Logo_cle.png'
SIMPLEUI_FAVICON="http://127.0.0.1:8000/static/favicon.ico"
# 自定义折叠栏
SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单，自定义菜单时建议关闭。
    'system_keep': False,

    # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。空列表[] 为全部不显示.
    'menu_display': ['用户管理', '花语管理', '鲜花管理', '订单管理', '权限管理'],

    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': False,
    'menus': [
        {
            'app': 'contents',
            'name': '花语管理',
            'icon': 'fa-solid fa-seedling',
            'models': [
                {
                    'name': '幻灯片管理',
                    'url': '/admin/contents/slide/',
                    'icon': 'fa-brands fa-dropbox'
                },
                {
                    'name': '花语管理',
                    'url': '/admin/contents/content/',
                    'icon': 'fa-solid fa-file-signature'
                },
                {
                    'name': '花语图片',
                    'icon': 'fa-solid fa-basket-shopping',
                    'url': '/admin/contents/contentimage/'
                }
            ]
        },
        {
            'app': 'users',
            'name': '用户管理',
            'models': [
                {
                    'name': '用户列表',
                    'icon': 'fas fa-user-shield',
                    'url': '/admin/users/user/'
                },
                {
                    'name': '地址管理',
                    'url': '/admin/users/address/'
                },
                {
                    'name': '用户组',
                    'icon': 'fa fa-th-list',
                    'url': 'auth/group/'
                }
            ]
        },
        {
            'app': 'goods',
            'name': '鲜花管理',
            'models': [
                {
                    'name': '类别管理',
                    'icon': 'fa fa-th-list',
                    'url': '/admin/goods/goodscategory/'
                },
                {
                    'name': '鲜花列表',
                    'icon': 'fa-solid fa-list',
                    'url': '/admin/goods/goods/'
                },
                {
                    'name': '主图管理',
                    'icon': 'fa-solid fa-image',
                    'url': '/admin/goods/goodimage/'
                },
                {
                    'name': '详情图管理',
                    'icon': 'fa-sharp fa-solid fa-images',
                    'url': '/admin/goods/detialimage/'
                }
            ]
        },
        {
            'app': 'orders',
            'name': '订单管理',
            'icon': 'fa-solid fa-tags',
            'models': [
                {
                    'name': '订单管理',
                    'icon': 'fa-solid fa-image',
                    'url': '/admin/orders/orderinfo/'
                },
                {
                    'name': '订单商品管理',
                    'icon': 'fa-sharp fa-solid fa-images',
                    'url': '/admin/orders/ordergoods/'
                }
            ]
        },
        {
            'app': 'auth',
            'name': '权限管理',
            'models': [
                {
                    'name': '用户权限',
                    'icon': 'fa-solid fa-image',
                    'url': '/admin/goods/goodimage/'
                },
            ]
        }
    ]
}