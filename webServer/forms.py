from django import forms
from apiServer.models import UserAndroid
from django.core.exceptions import ValidationError


class DownloadData (forms.Form):
    user = forms.ModelChoiceField(
        queryset=UserAndroid.objects.all(), empty_label="Pilih UUID")

    def clean_user(self):
        data = self.cleaned_data['user']
        uuid = data.uuid
        if UserAndroid.objects.filter(uuid=uuid).count() == 1:
            return data
