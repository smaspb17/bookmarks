import datetime

from django import forms
from django.contrib.auth import get_user_model

from account.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'email': 'E-mail',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпали')
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email существует')
        return email


class UserEditForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'E-mail',
        }

    def clean_email(self):
        # из поля в форме
        email = self.cleaned_data['email']
        # Queryset с совпадающими email из User, кроме текущего поль-ля
        qs = get_user_model().objects.exclude(
            email=self.instance.email).filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Такой email существует')
        return email


class ProfileEditForm(forms.ModelForm):
    this_year = datetime.date.today().year
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(
        years=tuple(range(this_year-100, this_year-5))), label='Дата рождения')

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
        labels = {
            'date_of_birth': 'Дата рождения',
            'photo': 'Фото',
        }






