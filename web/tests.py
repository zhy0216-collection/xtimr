import time

import ujson
from django.test import TestCase
from django.test.client import Client


class TestPostData(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_UDID='9527')

    def test_post_data(self):
        data = {
            "data": [{
                "url": "http://www.google.com/thisistest?hahah#nothing",
                "start_time": time.time(),
                "visit_length": 200 * 100 * 5, # mili_seconds
                }
            ]

        }



        r = self.client.post("/browse", {"data": ujson.dumps(data)})
        print r.content
        json_data = ujson.loads(r.content)
        self.assertTrue(json_data["success"])


