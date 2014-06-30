# -*- coding: utf-8 -*-
import datetime
import urlparse
from collections import defaultdict

from django.shortcuts import render

import datetime
import ujson


from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods

### local module

from web.models import WebUrl
from web.utils import parse_domain

# no timezone sofar
def get_browse_datetime(request):
    userid = request.META.get("HTTP_X_UDID")
    now = datetime.datetime.today()
    begin_time = datetime.date.today()
    end_time = begin_time + datetime.timedelta(days=1)
    urltimes = UrlTime.objects.filter(end_time__lte=end_time, start_time__gte=begin_time, userid=userid)
    # print "urltimes:%s"%urltimes
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
        d["details"] = [{"name": domain.title or domain.name,
                         "seconds": domain_sum[domain] / 1000} for domain in label_sum[label]]
        result.append(d)

    data = {"data":result, "total_time": sum([_["seconds"] for _ in result])}

    return HttpResponse(ujson.dumps(data), content_type="application/json")


@require_http_methods(["POST"])
def user_post_data(request):
    # TODO: consider timezone
    userid = request.META.get("HTTP_X_UDID")
    # print "request.META:%s"%request.META
    # print "data:%s"%request.POST
    # print "userid:%s"%userid

    data = request.POST["data"]
    data = ujson.loads(data)
    for url_time_dict in data["data"]:
        raw_url = url_time_dict["url"]
        domain_name = parse_domain(raw_url)
        path = urlparse.urlparse(raw_url).path
        web_url, created = WebUrl.objects.get_or_create(raw_url=raw_url, domain=domain, path=path)

        start_time = datetime.datetime.fromtimestamp(int(url_time_dict["start_time"])/1000)
        # print 'url_time_dict["start_time"]:%s'%url_time_dict["start_time"]
        # print "start_time:%s"%start_time
        milli_seconds = float(url_time_dict["milli_seconds"])
        # print "milli_seconds:%s"%url_time_dict["milli_seconds"]
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
        userid = request.META.get("HTTP_X_UDID")
        domain_id_list = [_["domain_id"] for _ in UrlTime.objects.filter(userid=userid).distinct("domain_id").values("domain_id")]
        domain_list = Domain.objects.filter(id__in=domain_id_list, label_id=1)
        label_list =[_.label for _ in domain_list]

        result = {
            "labels": [_.to_dict() for _ in label_list],
            "domains": [_.to_dict() for _ in domain_list],
            "success":True,
        }

        return HttpResponse(ujson.dumps(result),
                        content_type="application/json"
                    )

    elif request.method == "POST":
        pass


@require_http_methods(["POST"])
def create_label(request):
    name = request.POST.get("name")
    label = WebUrlLabel.get_or_create(name=name)
    result = {
        "success":True,
        "label_id":label.id
    }

    return HttpResponse(ujson.dumps(result),
                        content_type="application/json"
                    )

