from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from account.forms import LoginForm, UserRegistrationForm, UserEditForm, \
    ProfileEditForm
from account.models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Пользователь успешно '
                                        'аутентифицирован')
                else:
                    return HttpResponse('Не активный аккаунт')
            else:
                return HttpResponse('Не верный логин')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(reqeust):
    return render(reqeust, 'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.save(commit=False)
            user.set_password(cd['password'])
            user.save()
            Profile.objects.create(user=user)
            return render(request,
                          'account/register_done.html',
                          {'user': user})
    else:
        form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'form': form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form,
                          'profile_form': profile_form})
