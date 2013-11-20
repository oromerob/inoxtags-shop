#-*- coding:utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField

from transmeta import TransMeta


class PartnersHomeText(models.Model):
    __metaclass__ = TransMeta

    title = models.CharField(max_length=200)
    text = RichTextField()
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.title

    class Meta:
        translate = ('title', 'text',)
