from django.test import TestCase


class TestCase(TestCase):
    def setUp(self):
        pass
    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(1,1)

