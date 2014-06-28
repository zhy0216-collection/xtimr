# -*- coding: utf-8 -*-
from django.db import models


class WebUrl(models.Model):
    raw_url         = models.CharField(max_length=512)
    domain          = models.CharField(max_length=32)
    url_type        = models.CharField(max_length=32)

class UrlTime(models.Model):
    userid          = models.IntegerField()
    start_time      = models.DateTimeField()
    seconds         = models.IntegerField()
    web_url         = models.ForeignKey("WebUrl")


class WebUrlLabel(models.Model):
    name            = models.CharField(max_length=30)
    web_url         = models.ForeignKey("WebUrl")


class UserLabel(models.Model):
    name            = models.CharField(max_length=30)


