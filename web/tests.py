from django.test import TestCase
from django.test.client import Client


class TestPostData(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_UDID='9527')

    def test_post_data(self):
        self.assertEqual(1,1)

