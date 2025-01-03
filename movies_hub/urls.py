from django.contrib import admin
from django.urls import path, include, re_path
from debug_toolbar.toolbar import debug_toolbar_urls
from core.api import api

urlpatterns = ([
	re_path(r'^celery-progress/', include('celery_progress.urls')),
	path('admin/', admin.site.urls),
	path('api/', api.urls),
	path('', include('users.urls')),
	path('', include('movies.urls')),
	path('', include('social.urls')),
	path('', include('core.urls')),]
               + debug_toolbar_urls())
