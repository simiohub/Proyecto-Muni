from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .roles import ROLE_NAMES

User = get_user_model()


class UserAccountCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[(name, name) for name in ROLE_NAMES])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            group = Group.objects.get(name=self.cleaned_data['role'])
            user.groups.set([group])
        return user