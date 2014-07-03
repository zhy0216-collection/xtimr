import time

import ujson
from django.test import TestCase
from django.test.client import Client

from web.models import WebUrl, UrlTime

class TestPostData(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_UDID='9527')

    def test_post_data(self):
        data = {
            "data": [{
                "url": "http://www.google.com/thisistest?hahah#nothing",
                "start_time": time.time(),
                "milli_seconds": 200 * 100 * 5, # mili_seconds
                }
            ]

        }

        r = self.client.post("/browse", {"data": ujson.dumps(data)})
        # print r.content
        json_data = ujson.loads(r.content)
        self.assertTrue(json_data["success"])

        web_url = WebUrl.objects.all().first()
        self.assertEquals(web_url.domain, "www.google.com")
        self.assertEquals(web_url.path, "/thisistest")
        self.assertEquals(UrlTime.objects.count(), 1)











