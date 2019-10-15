from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', views.home),
    url(r'^$', views.home),
]

urlpatterns += staticfiles_urlpatterns()
