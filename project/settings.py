
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-rj35$p25z$nw)6*q5hlzbbcg=w@brtd9!@5(t%ygx0tl&$^c8r'
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'import_export',
    'rangefilter',
    #'axes',
    'crispy_forms',
    'crispy_bootstrap5',
    #'ckeditor', 
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'axes.middleware.AxesMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'project.urls'
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
                'adminlte2_templates.context_processors.template',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#settings za kawaida
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
import os
MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
STATICFILES_DIRS = [BASE_DIR / 'static']
LOGIN_REDIRECT_URL='/'
LOGIN_URL = '/administration/login/'
 


#ATOMIC_REQUESTS = False
#AXES_FAILURE_LIMIT = 3  # Number of login attempts allowed
#AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True  # Locks out the user after failure limit is reached
#AXES_COOLOFF_TIME = 24  # Lockout duration in hours (e.g., 24 hours)
#---------ends django axes--------------

#SESSION MAELEZO YAPO KWENYE INSTALLED APPS
#hii ni kwa ajili ya session expire kwamba account moja kutumika kwenye browser mbili
#au pc mbili,  ukilogin sehemu moja, sehemu nyingine inajitoa
#SESSION_SAVE_EVERY_REQUEST = True  # Refresh session on each request
#SESSION_COOKIE_SECURE = True
#SESSION_COOKIE_HTTPONLY = True
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_HTTPONLY = True



#AUTHENTICATION_BACKENDS = [
  #  'axes.backends.AxesBackend',  # Use AxesBackend for Django Axes version < 5.0
   #  'axes.backends.AxesStandaloneBackend',  # Use AxesStandaloneBackend for Django Axes version >= 5.0
   # 'django.contrib.auth.backends.ModelBackend',  # Default Django authentication backend
#]


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)

    # Logo to use for your site, must be present in static files, used for brand on top left

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
     "login_logo": "",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": False,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "ADMINISTRATION",

    # Copyright on the footer
    "copyright": "Ura Saccos LTD Version 1.0.0",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    #"search_model": [ "app.TimeTable", "app.CourseName"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        #{"name": "Support", "url": "support", "new_window": True},
        #{"name": "TimeTable", "url":"/", "new_window": False},
       # {"name": "Admin", "url":"admin:index", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "", "new_window": True},
        {"model": "auth.user", },
        {"model": "app.TimeTable", }
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
"icons": {
    "auth": "fa fa-users-cog text-white",
    "auth.user": "fa fa-user text-white",
    "auth.Group": "fa fa-users text-white",
    "app.Person": "fa fa-user text-white",
    "app.PersonReset": "fa fa-sync-alt text-white",  
    "app.Payroll": "fa fa-money-bill-wave text-white",
    "app.MessageLog": "fa fa-envelope text-white",
    "app.Employee": "fa fa-id-badge text-white",
    "app.District": "fa fa-map-marker-alt text-white",
    "app.Region": "fa fa-globe text-white",
    "app.Post": "fa fa-thumbtack text-white",
    "app.Role": "fa fa-user-tag text-white"


   
    },

    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "vertical_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": True,
    "brand_small_text": True,
    "brand_colour": "navbar-gray",
    "accent": "accent-lightblue",
    "navbar": "navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "sandstone",
    "dark_mode_theme": "slate",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}