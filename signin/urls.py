from django.conf.urls import url

from . import views

app_name = 'signin'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient_signin/$', views.patient_signin, name='patient_signin'),
    url(r'^find_patient/$', views.find_patient, name='find_patient'),
    url(r'^check_appointments/(?P<patient_id>.+)$', views.check_appointments, name='check_appointments'),
    url(r'^check_appointments/$', views.check_appointments, name='check_appointments'),
    url(r'^find_appointment/$', views.find_appointment, name='find_appointment'),
    url(r'^auth_redirect$', views.auth_redirect, name='auth_redirect'),
]