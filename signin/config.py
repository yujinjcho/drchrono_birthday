import os

# OAuth Settings for drchrono
development_mode = os.environ.get('DEVELOPMENT_MODE', 'False')

if development_mode == 'True':
    REDIRECT_BASE = 'http://127.0.0.1:8000/'
    CLIENT_ID = os.environ.get('CLIENT_ID', '')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '')
else:
    # Change this for production
    REDIRECT_BASE = ''
    CLIENT_ID = ''
    CLIENT_SECRET = ''

BASE_URL = 'https://drchrono.com/'

# End Points
PATIENTS = 'api/patients'
APPOINTMENTS = 'api/appointments'
ALLERGIES = 'api/allergies'
CURRENT_USER = 'api/users/current'
TOKEN = 'o/token/'
AUTH = 'o/authorize/'
REDIRECT = 'signin/auth_redirect'

# Allergy categories
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

# patient_form categories
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