from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetimewidget.widgets import DateTimeWidget
from datetimepicker.widgets import DateTimePicker
from .models import auction


class createAuction(forms.ModelForm):
    class Meta:
        model = auction
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'base_price']
        widgets = {'start_time': forms.DateTimeInput(widget=DateTimePicker(),),
                   'end_time': forms.DateTimeInput(attrs={'class': 'datetime-input'})}

# class createAuction(forms.Form):
#     title = forms.CharField()
#     base_price = forms.IntegerField()
#     # start_time = forms.DateTimeField(input_formats=['%Y/%m/%d %H:%M:%S'], widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M:%S'))
#     start_time = forms.DateTimeField(widget=DateTimePicker(),)
#     end_time = forms.DateTimeField(input_formats=['%Y/%m/%d %H:%M:%S'], widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M:%S'))
#     description = forms.CharField(widget=forms.Textarea())
#     location = forms.CharField(max_length=3)



class confAuction(forms.Form):
    CHOICES = [(x, x) for x in ("Yes", "No")]
    option = forms.ChoiceField(choices=CHOICES)
    title = forms.CharField(widget=forms.HiddenInput())


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user