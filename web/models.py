# -*- coding: utf-8 -*-
from django.db import models


class WebUrl(models.Model):
    name                    = models.CharField(max_length=32) # sina weibo
    raw_url                 = models.CharField(max_length=512)
    domain                  = models.CharField(max_length=128)
    path                    = models.CharField(max_length=256)

    def __unicode__(self):
        return self.raw_url

'''
# use path rule first, then domain rule

class PathRule(models.Model):
    # sina.com/read/ include bare domain, only first path
    domain                  = models.CharField(max_length=128)
    fisrt_path              = models.CharField(max_length=32)
    category_label          = models.ForeignKey("Label", default=1)
'''

# make simple solution firstly
class DomainRule(models.Model):
    domain                  = models.CharField(max_length=128) # sina.com weibo.com
    category_label          = models.ForeignKey("Label", default=1)

    def __unicode__(self):
        return self.domain + "===>" + self.category_label

class DomainDes(models.Model):
    domain                  = models.CharField(max_length=128)
    des_label               = models.ForeignKey("Label", default=1)


class UrlTime(models.Model):
    userid                  = models.CharField(max_length=64)
    start_time              = models.DateTimeField()
    milli_seconds           = models.IntegerField()
    end_time                = models.DateTimeField()
    web_url                 = models.ForeignKey("WebUrl")


# make label manager

class Label(models.Model):
    CATEGORY_TYPE           = 1
    DES_TYPE                = 2

    LABEL_TYPE_CHOICES      = (
            (CATEGORY_TYPE, "Category Type"),
            (DES_TYPE, "Descript Type"),
    )

    name            = models.CharField(max_length=32)
    label_type      = models.IntegerField(default=CATEGORY_TYPE,
                                          choices=LABEL_TYPE_CHOICES,)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }



