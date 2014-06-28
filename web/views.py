# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render

import datetime
import ujson


from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods

### local module

from web.models import WebUrl, Domain, UrlTime
from web.utils import parse_domain



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
            labels_of_domain = WebUrlLabel.objects.filter(domain__strartswith=_.name)
            domain_item_list =  label_dict[_]
            domain_item_list.append(_)
        except KeyError:
            domain_item_list =[]
            domain_item_list.append(_)
            d[_.label] = domain_ite_list

def _map_domain(urltimes):
    domain_dict = {}
    for _ in urltimes:
        try:
            url_list = domain_dict[_.domain]
            url_list.append(_)
        except KeyError:
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
        except KeyError:
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

@require_http_methods(["POST"])
def user_post_data(request):
    userid = request.META.get("HTTP_X_UDID")

    data = request.POST["data"]
    data = ujson.loads(data)
    print "data:%s"%data
    for url_time_dict in data["data"]:
        raw_url = url_time_dict["url"]
        domain_name = parse_domain(raw_url) 

        domain,created = Domain.objects.get_or_create(name=domain_name)
        web_url, created = WebUrl.objects.get_or_create(raw_url=raw_url, domain=domain)

        start_time = datetime.datetime.fromtimestamp(int(url_time_dict["start_time"])/1000)
        milli_seconds = float(url_time_dict["milli_seconds"])
        end_time = start_time + datetime.timedelta(seconds=milli_seconds/1000)

        result = {
            "userid": userid,
            "domain": domain,
            "web_url": web_url,
            "start_time": start_time,
            "milli_seconds": milli_seconds,
            "end_time": end_time,
        }

        url_time = UrlTime.objects.create(**result)

    return HttpResponse(ujson.dumps({"success":True}), 
                        content_type="application/json"
                    )


@require_http_methods(["GET", "POST"])
def readability(request):
    if request.method == "GET":
        url = request.GET.get("url") or None
        if url is None:
            raise Http404
        from readability.readability import Document
        import urllib
        html = urllib.urlopen(url).read()
        readable_article = Document(html).summary()

        return HttpResponse(readable_article)

