from django.test import TestCase

from . import views

class ConvertDate(TestCase):

    def test_convert_time_to_str(self):
        self.assertEqual(views.convert_time_to_str('02:30:00'),'2:30AM')
        self.assertEqual(views.convert_time_to_str('12:30:00'),'12:30PM')
        self.assertEqual(views.convert_time_to_str('13:30:00'),'1:30PM')
        self.assertEqual(views.convert_time_to_str('24:30:00'),'12:30AM')
        

class TestPhoneRegex(TestCase):

    def test_format_phone_number(self):
        self.assertEqual(views.format_phone_number('706-761-0743'), ('706','761','0743',''))
        self.assertEqual(views.format_phone_number('7067610743'), ('706','761','0743',''))
        self.assertEqual(views.format_phone_number('(706) 761 - 0743'), ('706','761','0743',''))
        self.assertEqual(views.format_phone_number('1 (706) 761 - 0743'), ('706','761','0743',''))
        self.assertEqual(views.format_phone_number('1-7067610743'), ('706','761','0743',''))
        self.assertEqual(views.format_phone_number('1-7067610743x323'), ('706','761','0743','323'))

    def test_format_phone_numbers(self):
        data_input = {'cell_phone':'444-444-4444', 'office_phone':'1-111-122-2432'}
        data_output = {'cell_phone':'(444) 444-4444', 'office_phone':'(111) 122-2432'}

        data_input2 = {'cell_phone':'444-444-4444 ext.123', 'office_phone':'1-111-122-2432', 'name': 'yujin'}
        data_output2 = {'cell_phone':'(444) 444-4444 x123', 'office_phone':'(111) 122-2432','name': 'yujin' }

        self.assertEqual(views.format_phone_numbers(data_input), data_output)
        self.assertEqual(views.format_phone_numbers(data_input2), data_output2)
