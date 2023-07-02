from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class SignUpForm(UserCreationForm):

    password2 = forms.PasswordInput

    class Meta:
        model=CustomUser
        fields=['first_name','last_name','phone_no','password1','password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2