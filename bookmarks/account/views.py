from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from account.forms import LoginForm, UserRegistrationForm, UserEditForm, \
    ProfileEditForm
from account.models import Profile, Contact

User = get_user_model()

def user_login(request):
    """Аутентификация и авторизация пользователя"""
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
    """Главная страница"""
    return render(reqeust, 'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    """Регистрация пользователя"""
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
    """Редактирование профиля пользователя (User + Profile)"""
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
            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Ошибка обновления профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form,
                          'profile_form': profile_form})


# @login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'account/user/list.html',
                  {'section': 'people', 'users': users})


# @login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html',
                  {'section': 'people', 'user': user})


@require_POST
@login_required
def user_follow(request):
    """Подписка на другого пользователя"""
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
