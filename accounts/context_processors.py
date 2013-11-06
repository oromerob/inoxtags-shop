#-*- coding:utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm

def auth_form(request):
    return {'AuthForm':AuthenticationForm,}


def cookies_agreement(request):

    try:
        Cookies = request.session['COOKIES_AGREEMENT']
    except:
        Cookies = None

    return {'Cookies':Cookies,}
