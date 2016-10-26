import re
import json
import requests
from datetime import datetime
from urllib import urlencode
import urlparse

from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required

from . import config


def index(request):
    '''login page for doctor'''

    query = {
        'redirect_uri': add_path_to_url(config.REDIRECT_BASE, config.REDIRECT),
        'response_type': 'code',
        'client_id': config.CLIENT_ID
    }
    url = add_path_to_url(config.BASE_URL, config.AUTH)
    DRCHRONO_REDIRECT = add_query_to_url(url, query)

    return render(
        request,
        'signin/index.html',
        {'DRCHRONO_REDIRECT': DRCHRONO_REDIRECT}
    )


def auth_redirect(request):
    '''directs user to auth server login'''

    req_data = {
        'code': request.GET.get('code'),
        'grant_type': 'authorization_code',
        'redirect_uri': add_path_to_url(config.REDIRECT_BASE, config.REDIRECT),
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
    }

    # Not using handle_api_request because we don't use
    # headers (access token) for this request
    response = requests.post(
        add_path_to_url(config.BASE_URL, config.TOKEN),
        data=req_data
    )
    data = response.json()
    request.session['access_token'] = data['access_token']
    handle_user(request, data['access_token'])
    return redirect('signin:patient_signin')


@login_required
def patient_signin(request):
    '''page for searching patients'''
    return render(request, 'signin/patient_signin.html')


@login_required
def find_patients(request):
    '''respond to POST request for patient info '''
    patients_data = get_patient_data(request)

    if patients_data:
        patient = patients_data[0]
    else:
        patient = None

    return JsonResponse(patient, safe=False)


@login_required
def check_appointments(request):
    '''redirects to appointments based on id '''

    patient_id = request.GET.get('appt_id')
    return redirect('signin:appointments', id=patient_id)


@login_required
def appointments(request, id):
    '''find appointments for given patient and current date '''

    appointment_data = get_appointment_data(request, id)
    data = transform_appointment_data(appointment_data["results"])
    return render(
        request,
        'signin/appointments.html',
        {"appointments": data, "patient_id": id}
    )


@login_required
def patient_form(request):
    '''provide form for patient data that is prepopulated '''
    patient_id = request.GET.get('patient_id')
    appt_id = request.GET.get('appt_id')
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
            "json_data": json_data,
            'patient_json': patient_json,
            'appt_id': appt_id
        }
    )


@login_required
def patient_form_submit(request):
    ''' handles form submission and updates patient information'''
    data = request.POST.copy()

    for key, value in data.iteritems():
        if 'phone' in key:
            data[key] = format_phone_number(value)

    url = add_path_to_url(config.BASE_URL, config.PATIENTS, data['patient_id'])
    response = handle_api_request(
        request=request,
        verb='patch',
        url=url,
        data=data
    )
    return HttpResponse('success')


@login_required
def allergies(request):
    '''Load patient allergy information'''

    patient = request.GET.get('patient')
    appt_id = request.GET.get('appt_id')

    response = handle_api_request(
        request=request,
        verb='get',
        url=add_path_to_url(config.BASE_URL, config.ALLERGIES),
        params={'patient': patient}
    )

    response.raise_for_status()
    allergies = response.json()
    allergy_types, reactions = get_allergy_categories()

    return render(
        request,
        'signin/allergies.html',
        {
            'allergies': allergies['results'],
            'allergy_types': allergy_types,
            'reactions': reactions,
            'patient_id': patient,
            'appt_id': appt_id,
            'allergies_json': json.dumps(allergies['results'])
        }
    )


@login_required
def update_allergies(request):
    '''Takes updated allergy information and saves to current
    current appointment notes.
    '''
    data = request.POST.copy()

    allergies_now_inactive = request.POST.getlist('set_inactive[]')
    new_allergies = json.loads(request.POST.get('new_allergies', ""))
    new_allergies_list = [
        allergy['reaction'] + ": " + allergy['notes']
        for allergy in new_allergies
    ]
    new_allergies_text = '. '.join(new_allergies_list)

    if allergies_now_inactive:
        inactive_allergies = ', '.join(allergies_now_inactive)
        updated_note = 'Inactive Allergies: %s. ' % inactive_allergies
    else:
        updated_note = ""

    if new_allergies:
        updated_note = updated_note + new_allergies_text

    url = add_path_to_url(
        config.BASE_URL,
        config.APPOINTMENTS,
        data['appointment_id']
    )

    response = handle_api_request(
        request=request,
        verb='patch',
        url=url,
        data={'notes': updated_note}
    )
    return HttpResponse(str(len(new_allergies)))


@login_required
def exit(request):
    '''Changes patient status to 'Arrived' and redirects to
    exit page
    '''
    appt_id = request.GET.get('appt_id')

    url = add_path_to_url(config.BASE_URL, config.APPOINTMENTS, appt_id)
    response = handle_api_request(
        request=request,
        verb='patch',
        url=url,
        data={'status': 'Arrived'}
    )

    return redirect('signin:exit_page')

    return render(
        request,
        'signin/exit.html'
    )

def exit_page(request):
    '''testing new exit page'''
    return render(request, 'signin/exit.html')

# helper functions
def add_query_to_url(url, query):
    '''accepts url and dict and returns encoded url'''

    url_parts = list(urlparse.urlparse(url))
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def add_path_to_url(url, *path):
    '''accepts url and path and returns encoded url'''

    url_parts = list(urlparse.urlparse(url))
    url_parts[2] = url_parts[2] + '/'.join([end for end in path])
    return urlparse.urlunparse(url_parts)


def format_phone_number(s):
    '''takes a variety of phone formats and returns in
    (XXX) XXX-XXXX format and appends an optional extension
    number.
    '''
    phone_pattern = re.compile(r'''
                # don't match beginning of string, number can start anywhere
    (\d{3})     # area code is 3 digits (e.g. '800')
    \D*         # optional separator is any number of non-digits
    (\d{3})     # trunk is 3 digits (e.g. '555')
    \D*         # optional separator
    (\d{4})     # rest of number is 4 digits (e.g. '1212')
    \D*         # optional separator
    (\d*)       # extension is optional and can be any number of digits
    $           # end of string
    ''', re.VERBOSE)

    try:
        if not phone_pattern.search(s):
            raise PhoneError("Inputted string didn't match")

        phone_num_groups = phone_pattern.search(s).groups()

        phone_text = '(%s) %s-%s' % (
            phone_num_groups[0],
            phone_num_groups[1],
            phone_num_groups[2]
        )

        if phone_num_groups[3]:
            phone_text = phone_text + ' x' + phone_num_groups[3]
    except PhoneError:
        return s

    return phone_text

class PhoneError(Exception):
    pass

def organize_forms():
    '''Returns patient fields in selected groupings'''

    return config.general, config.location, config.employer, config.contact


def transform_appointment_data(data):
    '''Adds AM and PM time format to each object '''
    for appointment in data:
        appointment['start_time'] = convert_time_to_str(
            appointment['scheduled_time']
        )

    return data


def get_user_data(request):
    '''Returns user(doctor's) information '''

    response = handle_api_request(
        request=request,
        verb='get',
        url=add_path_to_url(config.BASE_URL, config.CURRENT_USER)
    )
    data = response.json()
    return data


def get_appointment_data(request, patient_id):
    '''Returns appointment data for current day '''

    params = {
        'date': '-'.join([
            str(datetime.now().year),
            str(datetime.now().month),
            str(datetime.now().day)
        ]),
        'patient': patient_id
    }
    response = handle_api_request(
        request=request,
        verb='get',
        url=add_path_to_url(config.BASE_URL, config.APPOINTMENTS),
        params=params
    )

    data = response.json()
    return data


def handle_user(request, access_token):
    '''During Authorization process, create user
    if they don't exist.
     '''

    user_data = get_user_data(request)
    user_query = User.objects.filter(username=user_data['id'])

    if not user_query:
        user = User.objects.create_user(username=str(user_data['id']))
        user.save()
    else:
        user = user_query[0]

    login(request, user)


def get_patient_data(request):
    '''Returns patient data based on
    first name, last name, and date of birth
    '''

    patient_url = add_path_to_url(config.BASE_URL, config.PATIENTS)
    params = {
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'date_of_birth': request.POST.get('date_of_birth')
    }
    patients = []

    while patient_url:
        data = handle_api_request(
            request=request,
            verb='get',
            url=patient_url,
            params=params
        ).json()
        patients.extend(data['results'])

        # A JSON null on the last page
        patient_url = data['next']

    return patients


def handle_api_request(request, verb, url, params=None, data=None):
    '''handles api request and returns response

    :param str verb: accepts 'get', 'patch', and 'post'
    :param str url: url for endpoint
    :param dict data: data for 'patch' and 'post' requests
    '''

    headers = get_header(request)

    if verb == 'get':
        response = requests.get(
            url,
            params=params,
            headers=headers
        )
    elif verb == 'patch':
        response = requests.patch(
            url,
            data=data,
            headers=headers
        )
    elif verb == 'post':
        response = requests.post(
            url,
            data=data,
            headers=headers
        )

    response.raise_for_status()
    return response


def get_patient_by_id(request, patient_id):
    '''Returns patient by id '''
    url = add_path_to_url(config.BASE_URL, config.PATIENTS, patient_id)
    response = handle_api_request(
        request=request,
        verb='get',
        url=url
    )
    return response.json()


def convert_time_to_str(s):
    '''Adds AM and PM time format to object'''

    s_datetime_format = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    s_strformat = datetime.strftime(s_datetime_format, '%I:%M%p')
    return s_strformat


def get_header(request):
    '''return header with access token'''
    headers = {
        'Authorization': 'Bearer %s' % request.session['access_token'],
    }
    return headers


@register.filter
def get_item(dictionary, key):
    '''Allows template to access dictionary by key'''
    return dictionary.get(key)


@register.filter
def convert_to_title(str):
    '''Changes field from 'last_name' to 'Last Name' '''
    word_list = str.split('_')
    title_case = ' '.join([word.capitalize() for word in word_list])
    return title_case


def get_allergy_categories():
    '''return allergy categories and reactions'''
    return config.allergy_type, config.reaction
