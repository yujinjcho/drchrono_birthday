from django.test import TestCase

from . import views


class TestPhoneRegex(TestCase):

    def test_format_phone_number(self):
        self.assertEqual(
            views.format_phone_number('706-761-0743'),
            '(706) 761-0743'
        )
        self.assertEqual(
            views.format_phone_number('7067610743'),
            '(706) 761-0743'
        )
        self.assertEqual(
            views.format_phone_number('(706) 761 - 0743'),
            '(706) 761-0743'
        )
        self.assertEqual(
            views.format_phone_number('1 (706) 761 - 0743'),
            '(706) 761-0743'
        )
        self.assertEqual(
            views.format_phone_number('1-7067610743'),
            '(706) 761-0743'
        )
        self.assertEqual(
            views.format_phone_number('1-7067610743x323'),
            '(706) 761-0743 x323'
        )
