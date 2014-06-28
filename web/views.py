# -*- coding: utf-8 -*-
import datetime
from collections import defaultdict

from django.shortcuts import render

import datetime
import ujson


from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods

### local module

from web.models import WebUrl, Domain, UrlTime
from web.utils import parse_domain



# Create your views here.
def get_browse_datetime(request):
    now = datetime.datetime.today()
    begin_time = datetime.date.today()
    end_time = begin_time + datetime.timedelta(days=1)
    urltimes = UrlTime.objects.filter(end_time__lte=end_time, start_time__gte=begin_time)
    print "urltimes:%s"%urltimes
    url_times_list = [(_.domain, _.milli_seconds) for _ in urltimes]

    domain_sum = defaultdict(int)

    for domain, milli_seconds in url_times_list:
        domain_sum[domain] += milli_seconds

    result = []

    label_sum = defaultdict(list)
    for domain in domain_sum:
        label_sum[domain.label].append(domain)

    for label in label_sum:
        d = {"type": label.name}
        seconds = sum([domain_sum[_] for _ in label_sum[label]]) / 1000
        d["seconds"] = seconds 
        d["details"] = [{"name": domain.title,
                         "seconds": domain_sum[domain] / 1000} for domain in label_sum[label]]

    return HttpResponse(ujson.dumps(result), content_type="application/json")
 

# change me
def fake_get_user_type(request):
    response_data = {}

    response_data["type"] = u"新闻达人"
    response_data["label"] = [{"name": u"label1", "percent": 12}, 
                             {"name": u"label22", "percent": 22}]

    return HttpResponse(ujson.dumps(response_data), content_type="application/json")


@require_http_methods(["POST"])
def user_post_data(request):
    userid = request.META.get("HTTP_X_UDID")
    # print "request.META:%s"%request.META
    # print "data:%s"%request.POST
    # print "userid:%s"%userid

    data = request.POST["data"]
    data = ujson.loads(data)
    for url_time_dict in data["data"]:
        raw_url = url_time_dict["url"]
        domain_name = parse_domain(raw_url) 

        domain,created = Domain.objects.get_or_create(name=domain_name)
        web_url, created = WebUrl.objects.get_or_create(raw_url=raw_url, domain=domain)

        start_time = datetime.datetime.fromtimestamp(int(url_time_dict["start_time"])/1000)
        print 'url_time_dict["start_time"]:%s'%url_time_dict["start_time"]
        print "start_time:%s"%start_time
        milli_seconds = float(url_time_dict["milli_seconds"])
        print "milli_seconds:%s"%url_time_dict["milli_seconds"]
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

# test
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


@require_http_methods(["GET", "POST"])
def label_manage(request):
    if request.method == "GET":
        return render()

