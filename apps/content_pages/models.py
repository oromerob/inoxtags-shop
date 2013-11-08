#-*- coding:utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField

from transmeta import TransMeta


class HomeSlider(models.Model):
    __metaclass__ = TransMeta

    title = models.CharField(max_length=100)
    text = models.TextField()
    btn_link = models.CharField(max_length=50)
    btn_txt = models.CharField(max_length=50)
    img = models.ImageField(upload_to='img/')
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Homepage sliders"
        translate = ('title', 'text', 'btn_txt',)


class HomeFeaturette(models.Model):
    __metaclass__ = TransMeta

    slogan = models.CharField(max_length=100)
    subslogan = models.CharField(max_length=100)
    text = RichTextField()
    img = models.ImageField(upload_to='img/')
    img_desc = models.CharField(max_length=200)
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.slogan

    class Meta:
        verbose_name_plural = "Homepage featurettes"
        translate = ('slogan', 'subslogan', 'text', 'img_desc',)


class StaticPage(models.Model):
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100, verbose_name='name')
    title = models.CharField(max_length=100, verbose_name='title')
    content = RichTextField(verbose_name='content')

    def __unicode__(self):
        return self.name

    class Meta:
        translate = ('title', 'content',)
