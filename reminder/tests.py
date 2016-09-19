from datetime import datetime

from django.test import TestCase

from . import views

# Create your tests here.

class GroupPatients(TestCase):

    patient_data = [
        {'name': '1',
        'date_of_birth': '2016-09-13'},
        {'name': '2',
        'date_of_birth': '2016-09-19'},
        {'name': '3',
        'date_of_birth': '2016-10-10'},
        {'name': '4',
        'date_of_birth': '2016-08-01'},
        {'name': '5',
        'date_of_birth': '2016-09-15'},
    ]

    def test_group_patients(self):
        """check that group_patients is working correctly"""
        passed, upcoming = views.group_patients(GroupPatients.patient_data)
        passed_patients = [patient['name'] for patient in passed]
        upcoming_patients = [patient['name'] for patient in upcoming]

        self.assertEqual(passed_patients, ['5', '1'])
        self.assertEqual(upcoming_patients, ['2', '3', '4'])

