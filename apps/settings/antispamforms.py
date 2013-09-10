import time
from django import forms
from django.forms.util import ErrorDict
from django.conf import settings
from django.utils.hashcompat import sha_constructor

class AntiSpamModelForm(forms.ModelForm):
    timestamp     = forms.IntegerField(widget=forms.HiddenInput)
    security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)
    honeypot      = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'style':'display:none;'}),
                                    label='')
    
    def __init__(self, data=None, initial=None, instance=None):
        if initial is None:
            initial = {}
        initial.update(self.generate_security_data())
        super(AntiSpamModelForm, self).__init__(data=data, initial=initial, instance=instance)

    def security_errors(self):
        """Return just those errors associated with security"""
        errors = ErrorDict()
        for f in ["honeypot", "timestamp", "security_hash"]:
            if f in self.errors:
                errors[f] = self.errors[f]
        return errors

    def clean_security_hash(self):
        """Check the security hash."""
        security_hash_dict = {
            'timestamp' : self.data.get("timestamp", ""),
        }
        expected_hash = self.generate_security_hash(**security_hash_dict)
        actual_hash = self.cleaned_data["security_hash"]
        if expected_hash != actual_hash:
            raise forms.ValidationError("Security hash check failed.")
        return actual_hash

    def clean_timestamp(self):
        """Make sure the timestamp isn't too far (> 2 hours) in the past or too close (< 5 seg)."""
        ts = self.cleaned_data["timestamp"]
        difference = time.time() - ts
        if difference > (2 * 60 * 60) or difference < 5:
            raise forms.ValidationError("Timestamp check failed")
        return ts

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict =   {
            'timestamp'     : str(timestamp),
            'security_hash' : self.initial_security_hash(timestamp),
        }
        return security_dict

    def initial_security_hash(self, timestamp):
        """
        Generate the initial security hash from a (unix) timestamp.
        """

        initial_security_dict = {
            'timestamp' : str(timestamp),
          }
        return self.generate_security_hash(**initial_security_dict)

    def generate_security_hash(self, timestamp):
        """Generate a (SHA1) security hash from the provided info."""
        info = (timestamp, settings.SECRET_KEY)
        return sha_constructor("".join(info)).hexdigest()

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value
