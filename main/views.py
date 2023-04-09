import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Lobby_EN, Lobby_RU
from .forms import MainUserCreationForm, MainAuthenticationForm, Lobby_EN_Form, Lobby_RU_Form
from django.views import View
from django.contrib.auth import authenticate, login, logout


class MainView(View):
    def get(self, request):
        language = request.LANGUAGE_CODE
        if language == 'ru':
            LobbyForm = Lobby_RU_Form
            LobbyModel = Lobby_RU
            template = 'main/main_ru.html'
        else:
            LobbyForm = Lobby_EN_Form
            LobbyModel = Lobby_EN
            template = 'main/main_en.html'
        formLobby = LobbyForm(prefix='lobby')
        formRegistration = MainUserCreationForm(prefix='register')
        formLogin = MainAuthenticationForm(prefix='login')
        lobby = LobbyModel.objects.order_by('-created_at')
        context = {
            'formRegistration': formRegistration,
            'formLogin': formLogin,
            'formLobby': formLobby,
            'messages': lobby, 
        }
        if request.user.is_authenticated:
            user = request.user
            messages_en = Lobby_EN.objects.filter(user=user).order_by('-created_at')
            messages_ru = Lobby_RU.objects.filter(user=user).order_by('-created_at')
            context.update({'user': user, 'messages_en': messages_en, 'messages_ru': messages_ru})
        return render(request, template, context)

    def post(self, request):
        language = request.LANGUAGE_CODE
        if language == 'ru':
            LobbyForm = Lobby_RU_Form
            LobbyModel = Lobby_RU
            template = 'main/main_ru.html'
        else:
            LobbyForm = Lobby_EN_Form
            LobbyModel = Lobby_EN
            template = 'main/main_en.html'
        formLobby = LobbyForm(prefix='lobby')
        formRegistration = MainUserCreationForm(prefix='register')
        formLogin = MainAuthenticationForm(prefix='login')
        lobby = LobbyModel.objects.order_by('-created_at')
        if 'register' in request.POST:
            formRegistration = MainUserCreationForm(request.POST, prefix='register')
            if formRegistration.is_valid():
                formRegistration.save()
                user = authenticate(
                    request, 
                    username=formRegistration.cleaned_data['username'],
                    password=formRegistration.cleaned_data['password1']
                )
                if user:
                    login(request, user)
                    return redirect('main')
        elif 'login' in request.POST:
            formLogin = MainAuthenticationForm(request, data=request.POST, prefix='login')
            if formLogin.is_valid():
                user = authenticate(
                    request, 
                    username=formLogin.cleaned_data['username'],
                    password=formLogin.cleaned_data['password'],
                    remember_me=formLogin.cleaned_data['remember_me']
                )
                if user:
                    login(request, user)
                    if not formLogin.cleaned_data['remember_me']:
                        request.session.set_expiry(0)  
                    return redirect('main')
        elif 'logout' in request.POST:
            logout(request)
            return redirect('main')
        elif 'lobby' in request.POST:
            formLobby = LobbyForm(request.POST, prefix='lobby')
            if formLobby.is_valid():
                message = formLobby.save()
                message.user = request.user
                message.save()
                response_data = {'result': 'success', 'message': message.message_text}
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                response_data = {'result': 'error', 'message': 'Invalid form submission.'}
                return HttpResponse(json.dumps(response_data), content_type='application/json')
        context = {
            'formRegistration': formRegistration,
            'formLogin': formLogin,
            'formLobby': formLobby,
            'messages': lobby, 
        }
        if request.user.is_authenticated:
            user = request.user
            messages_en = Lobby_EN.objects.filter(user=user).order_by('-created_at')
            messages_ru = Lobby_RU.objects.filter(user=user).order_by('-created_at')
            context.update({'user': user, 'messages_en': messages_en, 'messages_ru': messages_ru})
        return render(request, template, context)








