from django.test import TestCase

from . import views

# Create your tests here.

class ConvertDate(TestCase):

    def test_convert_time_to_str(self):
        self.assertEqual(views.convert_time_to_str('02:30:00'),'2:30AM')
        self.assertEqual(views.convert_time_to_str('12:30:00'),'12:30PM')
        self.assertEqual(views.convert_time_to_str('13:30:00'),'1:30PM')
        self.assertEqual(views.convert_time_to_str('24:30:00'),'12:30AM')
        

