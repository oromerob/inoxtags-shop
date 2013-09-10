#-*- coding:utf-8 -*-
"""
Contact views.
"""

from django.views.generic.edit import CreateView
from django.core.mail import EmailMessage

from apps.contact.models import Contact
from apps.settings.models import ProjectSettings


class ContactFormView(CreateView):

    template_name = 'contact/contact_form.html'
    model = Contact
    success_url = "/contact/success/"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ContactFormView, self).get_context_data(**kwargs)
        # Add in the extra context
        context['contact_data'] = ProjectSettings.objects.values("phone","email","address","cp","town","country").get()
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an Httpresponse.
        title = "Missatge rebut a la pàgina web d'Inoxtags"
        content = 'Missatge de: ' + form.cleaned_data['name'] + ', ' + form.cleaned_data['email'] + "\n" + "\n"
        content += form.cleaned_data['message']
        mail = EmailMessage(title, content, to=['info@inoxtags.com'])
        mail.send()
        form.save()
        return super(ContactFormView, self).form_valid(form)
