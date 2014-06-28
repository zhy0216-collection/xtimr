from django.db import models


class WebUrl(models.Model):
    raw_url         = models.CharField(max_length=512)
    domain          = models.CharField(max_length=32)
    description     = models.CharField(max_length=512)

class WebLabel(models.Model):
    name            = models.CharField(max_length=30)
    


class PersonLabel(models.Model):
    name            = models.CharField(max_length=30)


