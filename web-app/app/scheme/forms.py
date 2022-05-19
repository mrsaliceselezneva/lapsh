from .models import Therm, Connection, XmlFile
from django.forms import ModelForm, TextInput, Textarea


class ThermForm(ModelForm):
    class Meta:
        model = Therm
        fields = ['title', 'body', 'image', 'mark']

        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'название'
            }),
            'body': Textarea(attrs={
                'placeholder': 'определение'
            }),
            'mark': TextInput(attrs={
                'placeholder': 'обозначение'
            }),
        }


class ConnectionForm(ModelForm):
    class Meta:
        model = Connection
        fields = ['title', 'body', 'image', 'mark']

        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'название'
            }),
            'body': Textarea(attrs={
                'placeholder': 'определение'
            }),
            'mark': TextInput(attrs={
                'placeholder': 'обозначение'
            }),
        }


class XMLForm(ModelForm):
    class Meta:
        model = XmlFile
        fields = ['title', 'file']

        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'название'
            }),
        }
