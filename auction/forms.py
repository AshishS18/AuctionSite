from crispy_forms.bootstrap import InlineRadios, TabHolder, Tab
from crispy_forms.layout import Layout, Field, Fieldset, Div
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetimepicker.widgets import DateTimePicker

from .models import auction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class createAuction(forms.ModelForm):
    class Meta:
        model = auction
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'base_price', 'image']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'}),
                   'start_time': forms.DateTimeInput(attrs={'class': 'datetimepicker1','class': 'form-control'}),
                   'end_time': forms.DateTimeInput(attrs={'class': 'datetimepicker1','class': 'form-control'}),
                   'location': forms.TextInput(attrs={'class': 'form-control'}),
                   'base_price': forms.TextInput(attrs={'class': 'form-control'}),
                   'image': forms.FileInput(attrs={'class': 'form-control'})}
        helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(createAuction, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        helper = FormHelper()



    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user