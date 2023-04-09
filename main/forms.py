from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MainUser, Lobby_EN, Lobby_RU
from django.core.exceptions import ValidationError
import random
import re


class MainUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        while True:
            new_id = str(random.randint(10000000, 99999999))
            if not MainUser.objects.filter(username=new_id).exists():
                break
        self.fields['username'].initial = new_id


    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'hero-settings-user-window-registration-username',
            'placeholder': 'ID',
            'readonly': 'readonly',
        }),
        required=True,
        min_length=8,
        max_length=8,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'hero-settings-user-window-registration-password', 
            'placeholder':'Пароль'
        }),
        required=True,
        min_length=8,
        max_length=128,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'hero-settings-user-window-registration-password', 
            'placeholder':'Подтвердить пароль'
        }),
        required=True,
        min_length=8,
        max_length=128,
    )

    error_messages = {
        'password_mismatch': 'Пароли не совпадают.',
        'password_too_short': 'Пароль не должен содержать менее %(min_length)s символов.',
        'password_common_words': '',
        'password_entirely_numeric': '',
        'username_already_exists': 'Пользователь с таким ID уже существует.',
        'null': 'Это поле не должно быть пустым.',
        'blank': 'Это поле не должно быть пустым.',
        'min_length': 'Это поле не должно содержать менее %(min)d символов.',
        'max_length': 'Это поле не должно содержать более %(max)d символов.',
        'required': 'Это поле обязательно.'
    }

    class Meta:
        model = MainUser
        fields = ('username', 'password1', 'password2')


    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) != 8:
            raise ValidationError('ID должен состоять ровно из 8 цифр.')
        if not username.isdigit():
            raise ValidationError('ID должен содержать только цифры.')
        if MainUser.objects.filter(username=username).exists():
            raise ValidationError(
                self.error_messages['username_already_exists'],
                code='username_already_exists'
            )
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=[\]{}|;:\'",./<>?]+$', password1):
            raise ValidationError('Пароль не должен содержать некорректные символы.')
        return password1

class MainAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'hero-settings-user-window-login-username',
            'placeholder': 'ID',
        }),
        required=True,
        min_length=8,
        max_length=8,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'hero-settings-user-window-login-password', 
            'placeholder':'Пароль'
        }),
        required=True,
        min_length=8,
        max_length=128,
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'checked': 'checked',
            'id': 'remember_me-checkbox'
        }),
        required=False,
    )

    error_messages = {
        'invalid_login': 'Неверный ID или пароль.',
    }

    class Meta:
        model = MainUser
        fields = ('username', 'password')


class Lobby_EN_Form(forms.ModelForm):
    message_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'hero-feed-send-input',
            'name': 'hero-feed-send-input',
            'class': 'hero-feed-send-input',
            'placeholder': 'Type here...',
        }),
        required=True,
        min_length=100,
        max_length=30000,
    )
    error_messages = {
        'required': 'This field is required.',
        'min_length': 'The message must be at least 100 characters long.',
        'max_length': 'The message must not be longer than 30000 characters.',
    }

    class Meta:
        model = Lobby_EN
        fields = ['message_text']

    def clean_message_text(self):
        message_text = self.cleaned_data['message_text']
        if len(message_text) < 100:
            raise ValidationError(
                self.error_messages['min_length'],
                code='min_length'
            )
        return message_text

class Lobby_RU_Form(forms.ModelForm):
    message_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'hero-feed-send-input',
            'name': 'hero-feed-send-input',
            'class': 'hero-feed-send-input',
            'placeholder': 'Пишите здесь...',
        }),
        required=True,
        min_length=100,
        max_length=30000,
    )
    error_messages = {
        'required': 'Это поле обязательно.',
        'min_length': 'Сообщение должно содержать не менее 100 символов.',
        'max_length': 'Сообщение должно содержать не более 30000 символов.',
    }

    class Meta:
        model = Lobby_RU
        fields = ['message_text']

    def clean_message_text(self):
        message_text = self.cleaned_data['message_text']
        if len(message_text) < 100:
            raise ValidationError(
                self.error_messages['min_length'],
                code='min_length'
            )
        return message_text
