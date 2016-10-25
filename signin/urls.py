
from django.conf.urls import url

from . import views

app_name = 'signin'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient_signin/$', views.patient_signin, name='patient_signin'),
    url(r'^find_patient/$', views.find_patients, name='find_patient'),
    url(
        r'^check_appointments/$',
        views.check_appointments,
        name='check_appointments'
    ),
    url(r'^patient_form/$', views.patient_form, name='patient_form'),
    url(
        r'^patient_form_submit/$',
        views.patient_form_submit,
        name='patient_form_submit'
    ),
    url(r'^allergies/$', views.allergies, name='allergies'),
    url(
        r'^update_allergies/$',
        views.update_allergies,
        name='update_allergies'
    ),
    url(r'^exit/$', views.exit, name='exit'),
    url(r'^auth_redirect$', views.auth_redirect, name='auth_redirect'),
]
