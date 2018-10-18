from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetimepicker.widgets import DateTimePicker

from .models import auction
from crispy_forms.helper import FormHelper


class createAuction(forms.ModelForm):
    # class Meta:
    #     model = auction
    #     fields = ['title', 'description', 'start_time', 'end_time', 'location', 'base_price']
    #     widgets = {'start_time': forms.DateTimeInput(widget=DateTimePicker(),),
    #                'end_time': forms.DateTimeInput(attrs={'class': 'datetime-input'})}

    class Meta:
        model = auction
        helper = FormHelper()
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'base_price', 'image']
        widgets = {'start_time': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
                   'end_time': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
                   }



class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        helper = FormHelper()
        fields = ("username", "email", "password1", "password2")
        widgets = {'username': forms.TextInput(attrs={ 'class': 'form-control'}),
                   'email': forms.TextInput(attrs={ 'class': 'form-control'}),
                   'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
                   'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
                   }


    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user