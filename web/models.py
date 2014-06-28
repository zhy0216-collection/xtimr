# -*- coding: utf-8 -*-
from django.db import models


class WebUrl(models.Model):
    raw_url         = models.CharField(max_length=512)
    domain          = models.ForeignKey("Domain")


class Domain(models.Model):
    name         = models.CharField(max_length=64)


class UrlTime(models.Model):
    userid          = models.IntegerField()
    start_time      = models.DateTimeField()
    milli_seconds   = models.IntegerField()
    end_time        = models.DateTimeField()
    web_url         = models.ForeignKey("WebUrl") # maybe useful
    domain          = models.ForeignKey("Domain")


class WebLabelCategory(models.Model):
    name            = models.CharField(max_length=32)


class WebUrlLabel(models.Model):
    name            = models.CharField(max_length=32)
    domain          = models.ForeignKey("Domain")
    category        = models.ForeignKey("WebLabelCategory", null=True)


class UserLabel(models.Model):
    name            = models.CharField(max_length=32)


