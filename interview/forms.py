from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    access_code = forms.CharField(label="Access code")

    class Meta:
        model = User
        # fields = ("username", "email", "password1", "password2")
        fields = ("username", "password1", "password2", "access_code")
        labels = {
            "username": "Email",
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
