# -*- coding: utf-8 -*-
from django.db import models


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class BasicItemModel(TimeStampedModel):
    class Meta:
        abstract = True

    name = models.CharField(
        u'이름', max_length=255, blank=True, default='')
    uid = models.CharField(
        u'UID', max_length=255, unique=True, )
    description = models.CharField(
        u'설명', max_length=255, blank=True, default='')
