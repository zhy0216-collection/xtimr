# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import datetime




import ujson



from .models import *
# Create your views here.
def get_browser_datetime():
    begin_time = datetime.datetime()

def fake_get_user_type(request):
    response_data = {}

    response_data["type"] = u"新闻达人"
    response_data["label"] = [{"name": u"label1", "percent": 12}, 
                             {"name": u"label22", "percent": 22}]

    return HttpResponse(ujson.dumps(response_data), content_type="application/json")

def fake_get_browse_datetime(request):
    response_data = {}

    response_data["total_time"] = 3000
    response_data["data"] = [{"type": u"新闻", "seconds": 30}, 
                             {"type": u"娱乐", "seconds": 50}]

    return HttpResponse(ujson.dumps(response_data), content_type="application/json")

