#-*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("name"), blank=True)
    email = models.EmailField()
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message[:50]
