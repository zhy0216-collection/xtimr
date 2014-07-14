import time

import ujson
from django.test import TestCase
from django.test.client import Client
from model_mommy import mommy

from web.models import WebUrl, UrlTime

class TestPostData(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_UDID='9527')
        self.label = mommy.make("Label", id=1)

    def test_post_data(self):
        data = {
            "data": [{
                "url": "http://www.google.com/thisistest?hahah#nothing",
                "start_time": time.time(),
                "total_milli_seconds": 200 * 100 * 5, # mili_seconds
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
        # print "UrlTime.objects:%s"%UrlTime.objects.all().first()

    def test_get_browse_datetime_by_category_label(self):
        data = {
            "data": [{
                    "url": "http://www.google.com/thisistest?hahah#nothing",
                    "start_time": time.time() * 1000,
                    "total_milli_seconds": 200 * 100 * 5, # mili_seconds
                }, {
                    "url": "http://www.google.com/thisistest?hahah#nothing",
                    "start_time": time.time(),
                    "total_milli_seconds": 200 * 100 * 5, # mili_seconds
                }
            ]

        }

        self.client.post("/browse", {"data": ujson.dumps(data)})
        r = self.client.get("/show_data_by_category")

        data = ujson.loads(r.content)

        self.assertTrue(self.label.name in data["labels"])

