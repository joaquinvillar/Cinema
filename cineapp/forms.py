from django import forms
from .models import Document


class SignForm(forms.Form):
    your_name = forms.CharField(label='Username', max_length=100)
    your_pass = forms.CharField(label='Password', max_length=100)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
