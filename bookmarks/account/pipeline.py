from django.contrib.auth.models import Group
from django.contrib.auth import logout

from account.models import Profile


def new_users_handler(backend, user, response, *args, **kwargs):
    """
    Пайплайн добавления social-аккаунта в группу social, а также
    автоматическое создание Профиля пользователя.
    """
    group = Group.objects.filter(name='social')
    if len(group):
        user.groups.add(group[0])
    Profile.objects.get_or_create(user=user)


#
def social_user(backend, uid, user=None, request=None, *args, **kwargs):
    """
    Пайплайн выхода из social-аккаунта при входе в другой social-аккаунт.
    """
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)

    if social:
        if user and social.user != user:
            logout(request)
        user = social.user

    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}




