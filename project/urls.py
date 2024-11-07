"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('administration/', admin.site.urls),
    path('', include("app.urls")),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    
]
from django.contrib import admin

admin.site.site_header = "URA-MOBILE"
admin.site.index_title = "URA-MOBILE"
admin.site.site_title = "AURA-MOBILE"

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
 