import json
import requests
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from . import drchrono_config
from .models import Message

# Create your views here.
def index(request):
    DRCHRONO_REDIRECT = "https://drchrono.com/o/authorize/?redirect_uri=%s&response_type=code&client_id=%s" % (drchrono_config.REDIRECT_URI, drchrono_config.CLIENT_ID)
    return render(
        request,
        'reminder/index.html',
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
    access_token = data['access_token']
    handle_user(request, access_token)
    return redirect('reminder:birthdays', access=access_token)
    
@login_required
def birthdays(request, access):
    data = get_patient_data(access)
    recently_passed, upcoming = group_patients(data)
    
    if upcoming:
        current_patient = upcoming[0]
    else:
        current_patient = None
    return render(
        request, 
        'reminder/birthdays.html', 
        {
            'passed': recently_passed,
            'upcoming': upcoming,
            'patient_data': recently_passed + upcoming,
            'patient_data_json': json.dumps(recently_passed + upcoming)
        }
    )

@login_required
def create_message(request):
    current_user = request.user
    new_message = Message(
        user=current_user,
        patient_id = request.POST.get('patient_id'),
        creation_date = datetime.now()
    )
    new_message.save()
    return HttpResponse("Created Successfully")


#Helper functions
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

def handle_user(request, access_token):
    user_data = get_user_data(access_token)
    user_query = User.objects.filter(username=user_data['id'])

    if not user_query:
        user = User.objects.create_user(username=str(user_data['id']))
        user.save()
    else:
        user = user_query[0]
    
    login(request, user)

def get_patient_data(access_token):
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }
    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page

    return patients

def group_patients(patient_data):
    
    # Currently excluding patients without dob data
    patient_data = [
        patient for patient in patient_data 
        if patient["date_of_birth"]
    ]

    date_now = datetime.now()
    current_date = datetime(date_now.year, date_now.month, date_now.day)
    
    recently_passed = []
    upcoming_birthdays = []

    #Determine appropriate date range for birthday greetings
    PAST_BDAY_RANGE = -14
    FUTURE_BDAY_RANGE = 340

    for patient in patient_data:
        bday = datetime.strptime(
            patient['date_of_birth'], '%Y-%m-%d'
        )
        bday_this_year = datetime(current_date.year, bday.month, bday.day)
        days_diff = bday_this_year - current_date

        # add days diff for sorting and display purposes
        if days_diff.days < 0 and days_diff.days >= PAST_BDAY_RANGE:
            patient['days_since_bday'] = days_diff.days
            recently_passed.append(patient)
        else:
            # if birthday already passed, add next year day diff
            if days_diff.days >= 0:
                patient['days_to_bday'] = days_diff.days
                
            else:
                bday_next_year = datetime(current_date.year + 1, bday.month, bday.day)
                days_to_bday = bday_next_year - current_date
                patient['days_to_bday'] = days_to_bday.days

            # only include if birthday is coming up in FUTURE_RANGE days
            if patient['days_to_bday'] <= FUTURE_BDAY_RANGE:
                upcoming_birthdays.append(patient)

    recently_passed.sort(key=lambda x: x['days_since_bday'])
    upcoming_birthdays.sort(key=lambda x: x['days_to_bday'])

    return recently_passed[::-1], upcoming_birthdays
    