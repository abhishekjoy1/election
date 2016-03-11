import re
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from models import CustomUser, State, Seat, Booth
import pdb

class RegistrationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def __init__(self, *args, **kwargs):
      super(RegistrationForm, self).__init__(*args, **kwargs)

      # check state in POST data and change qs
      if 'state' in self.data:
          self.fields['seat'].queryset = Seat.objects.filter(state=self.data.get('state'))
      if 'seat' in self.data:
          self.fields['booth'].queryset = Booth.objects.filter(seat=self.data.get('seat'))

    state = forms.ModelChoiceField(State.objects.all())
    seat = forms.ModelChoiceField(Seat.objects.none())
    booth = forms.ModelChoiceField(Booth.objects.none())
    first_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("First name"), error_messages={ 'invalid': _("This value must contain only letters") })
    last_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Last name"), error_messages={ 'invalid': _("This value must contain only letters") })
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs= {'class':'datepicker'}))
    sex = forms.ChoiceField(choices=(('M', 'MALE'), ('F', 'FEMALE')), label=_("Sex"))
    voter_id = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Voter Id"))
    is_election_staff = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = CustomUser
        fields = ['state', 'seat', 'booth', 'first_name', 'last_name', 'voter_id', 'date_of_birth', 'sex', 'is_election_staff']


    def clean_username(self):
        try:
            user = User.objects.get(voter_id__iexact=self.cleaned_data['voter_id'])
        except User.DoesNotExist:
            return self.cleaned_data['voter_id']
        raise forms.ValidationError(_("The user with given voter id already exists. Please try another one."))



    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.sex = self.cleaned_data['sex']
        user.voter_id = self.cleaned_data['voter_id']
        user.is_election_staff = self.cleaned_data['is_election_staff']
        user.username = user.voter_id
        user.booth = self.cleaned_data['booth']
        # user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user