import json
import requests
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from . import drchrono_config

from django.template.defaulttags import register

def index(request):
    DRCHRONO_REDIRECT = "https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s" % (drchrono_config.REDIRECT_URI, drchrono_config.CLIENT_ID)
    return render(
        request,
        'signin/index.html',
        {'DRCHRONO_REDIRECT': DRCHRONO_REDIRECT}
    )

def auth_redirect(request):
    code = request.GET.get('code')
    response = requests.post('https://drchrono.com/o/token/', data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': drchrono_config.REDIRECT_URI,
        'client_id': drchrono_config.CLIENT_ID,
        'client_secret': drchrono_config.CLIENT_SECRET,
    })
    response.raise_for_status()
    data = response.json()
    request.session['access_token'] = data['access_token']
    handle_user(request, data['access_token'])
    return redirect('signin:patient_signin')

@login_required
def patient_signin(request):
    return render(request, 'signin/patient_signin.html')

@login_required
def find_patients(request):
    patients_data = get_patient_data(request)

    if patients_data:
        patient = patients_data[0]
    else:
        patient = None
    
    return JsonResponse(patient, safe=False)

@login_required
def check_appointments(request):
    patient_id = request.GET.get('id')
    appointment_data = get_appointment_data(request.session['access_token'], patient_id)
    data = transform_appointment_data(appointment_data["results"])
    return render(
        request, 
        'signin/appointments.html', 
        {"appointments":data, "patient_id":patient_id}#
    )

@login_required
def patient_form(request):
    patient_id = request.GET.get('patient_id')
    patient = get_patient_by_id(request, patient_id)
    general, location, employer, contact = organize_forms()
    json_data = json.dumps(general + location + employer + contact)
    patient_json = json.dumps(patient)

    return render(
        request,
        'signin/patient_form.html',
        {
            'general': general,
            'location': location,
            'employer': employer,
            'contact': contact,
            'patient': patient,
            "json_data" : json_data,
            'patient_json': patient_json
        }
    )

@login_required
def patient_form_submit(request):
    data = request.POST.copy()
    url = 'https://drchrono.com/api/patients/' + data['patient_id']
    r = requests.put(url, data=data, headers=get_header(request))
    r.raise_for_status()
    return HttpResponse('success')

########################################
########################################
########################################
########################################

@login_required
def allergies(request):
    patient = request.GET.get('patient')
    
    response = requests.get(
        'https://drchrono.com/api/allergies', 
        params= {'patient': patient},
        headers=get_header(request)
    )

    response.raise_for_status()
    allergies = response.json()
    allergy_types, reactions = get_allergy_categories()

    return render(
        request, 
        'signin/allergies.html',
        {
            'allergies': allergies['results'],
            'allergy_types':allergy_types,
            'reactions': reactions
        }
    )

########################################
########################################
########################################
########################################

@login_required
def exit(request):
    return render(
        request, 
        'signin/exit.html'
    )



#helper functions
def organize_forms():
    general = [
        'first_name',
        'last_name',
        'middle_name'
    ]
    location = ['address', 'city', 'state', 'zip_code']
    employer = [
        'employer',
        'employer_address', 
        'employer_city', 
        'employer_state', 
        'employer_zip_code'
    ]
    contact = [
        'cell_phone',
        'home_phone',
        'email',
        'emergency_contact_name',
        'emergency_contact_phone',
        'emergency_contact_relation',
        'responsible_party_name',
        'responsible_party_relation',
        'responsible_party_phone',
        'responsible_party_email'
    ]

    return general, location, employer, contact


def get_geographical_data():
    data = ['address', 'city', 'state', 'zip_code']
    return data

def transform_appointment_data(data):
    for appointment in data:
        appointment['start_time'] = convert_time_to_str(appointment['scheduled_time'][-8:])

    return data

def get_user_data(access_token):
    response = requests.get(
        'https://drchrono.com/api/users/current', 
        headers={
            'Authorization': 'Bearer %s' % access_token,
        }
    )
    response.raise_for_status()
    data = response.json()
    return data

def get_appointment_data(access_token, patient_id):
    now = datetime.now()
    today = '-'.join([str(now.year), str(now.month), str(now.day)])

    response = requests.get(
        'https://drchrono.com/api/appointments', 
        params={"date":today,"patient":patient_id},
        headers={
            'Authorization': 'Bearer %s' % access_token
        }
    )

    response.raise_for_status()
    data = response.json()
    return data

def handle_user(request, access_token):
    user_data = get_user_data(access_token)
    user_query = User.objects.filter(username=user_data['id'])

    if not user_query:
        user = User.objects.create_user(username=str(user_data['id']))
        user.save()
    else:
        user = user_query[0]
    
    login(request, user)

def get_patient_data(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    date_of_birth = request.POST.get('date_of_birth')

    headers = {
        'Authorization': 'Bearer %s' % request.session['access_token'],
    }
    patients = []

    query_params = (date_of_birth, first_name, last_name)
    query_url = '?date_of_birth=%s&first_name=%s&last_name=%s' % query_params
    patients_url = 'https://drchrono.com/api/patients' + query_url
    
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page

    return patients

def get_patient_by_id(request, patient_id):
    headers = {
        'Authorization': 'Bearer %s' % request.session['access_token'],
    }
    patients_url = 'https://drchrono.com/api/patients'
    data = requests.get(patients_url, headers=headers).json()
    all_patients = data['results']
    #Doesn't look can query API for patient_id
    patient = [patient for patient in all_patients if patient['id'] == int(patient_id)]
    return patient[0]

def get_current_date(datetime_obj):
    date_now = datetime_obj
    return datetime(date_now.year, date_now.month, date_now.day)

def convert_time_to_str(s):
    h_m_s = s.split(":")
    hour, minutes, seconds = [int(metric) for metric in h_m_s]

    if hour <= 23 and hour >= 12:
        time_of_day = "PM"
    else:
        time_of_day = "AM"

    if hour >= 13:
        hour = hour - 12

    return "%d:%02d%s" % (hour,minutes, time_of_day)

def get_header(request):
    headers={
        'Authorization': 'Bearer %s' % request.session['access_token'],
    }
    return headers

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def convert_to_title(str):
    word_list = str.split('_')
    title_case = ' '.join([word.capitalize() for word in word_list])
    return title_case

def get_allergy_categories():

    allergy_type = [
        'Specific Drug allergy',
        'Drug Class allergy',
        'Non-Drug allergy',
        'No Known Drug Allergies (NKA)'
    ]
        
    reaction = [
        'Acute kidney failure',
        'Arthralgia',
        'Chills',
        'Cough',
        'Fever',
        'Headache',
        'Hives',
        'Malaise/fatigue',
        'Myalgia',
        'Nasal congestion',
        'Nasuea',
        'Pain/soreness at injection site',
        'Rash',
        'Respiratory distress',
        'Rhinorrhea',
        'Shortness of breath/difficulty breathing',
        'Sore throat',
        'Swelling'
    ]    

    return allergy_type, reaction
