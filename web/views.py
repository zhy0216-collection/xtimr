# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import datetime




import ujson



from .models import *




# Create your views here.
def get_browser_datetime():
    now = datetime.datetime.today()
    begin_time = datetime.date.today()
    end_time = begin_time + datetime.timedelta(1)
    urltimes = UrlTime.objects.filter(end_time__lte=endtime, end_time__bte=begin_time)
    urltimes_uniq = _urltimes_uniq(urltimes)
    domain_list = _map_domain(urltimes_uniq)
    label_list =  _map_label(domain_list)

    return ujson.dump(label_list)



    

def _map_label(domain_list):
    label_dict ={}
    for _ in domain_list:
        try:
            labels_of_domain = WebUrlLabel.objects.filter(domain__strartswith=_.content)
            
            domain_item_list =  label_dict[_]
            domain_item_list.append(_)
        catch KeyError:
            tmp = =[]
            tmp.append(_)
            d[_.label] = tmp

def _map_domain(urltimes):
    domain_dict = {}
    for _ in urltimes:
        try:
            
            url_list = domain_dict[_.domain]
            url_list.append(_)
            
        catch KeyError:
            url_list = []
            url_list.appent(_)
            d[_.domain] = url_list
    return domain_dict
        
def _urltimes_uniq(urltimes):
    d = {}
    for url_time in urltimes:
        try:
            item = d[url_time.web_url]
            item.seconds += url_time.seconds
        catch KeyError:
            d[url_time.web_url] = url_time
     return d

def fake_get_user_type(request):
    response_data = {}

    response_data["type"] = u"新闻达人"
    response_data["label"] = [{"name": u"label1", "percent": 12}, 
                             {"name": u"label22", "percent": 22}]

    return HttpResponse(ujson.dumps(response_data), content_type="application/json")

def fake_get_browse_datetime(request):
    response_data = {}

    response_data["total_time"] = 100
    response_data["data"] = [{"type": u"新闻", "seconds": 30}, 
                             {"type": u"娱乐", "seconds": 50}]

    return HttpResponse(ujson.dumps(response_data), content_type="application/json")

