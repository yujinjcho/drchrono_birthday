from django.conf.urls import url

from . import views

app_name = 'reminder'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^birthdays/(?P<access>.+)$', views.birthdays, name='birthdays'),
    url(r'^auth_redirect$', views.auth_redirect, name='auth_redirect'),
    url(r'^create_message$', views.create_message, name='create_message'),
]