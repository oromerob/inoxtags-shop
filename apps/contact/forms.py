# -*- coding:utf-8 -*-

from apps.settings.antispamforms import AntiSpamModelForm

from apps.contact.models import Contact


class ContactForm(AntiSpamModelForm):

    class Meta:
        model = Contact

    def send_mail(self):
        pass
