#-*- coding:utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm

def auth_form(request):
    return {'AuthForm':AuthenticationForm,}
