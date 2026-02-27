from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Game


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ThemeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('dark_background',)


class GameFilterForm(forms.Form):
    title = forms.CharField(required=False)
    genre = forms.ChoiceField(
        choices=[('', 'Всі')] + Game.GENRE_CHOICES,
        required=False
    )
    sort_by_price = forms.ChoiceField(
        choices=[
            ('', 'Без сортування'),
            ('asc', 'Дешеві → дорогі'),
            ('desc', 'Дорогі → дешеві'),
        ],
        required=False
    )
