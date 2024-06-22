from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse, reverse_lazy, include

from account import views


urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('password-change/',
    #      PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password-change/done/',
    #      PasswordChangeDoneView.as_view(),
    #      name='password_change_done'),
    # path("password-reset/",
    #      PasswordResetView.as_view(),
    #      name="password_reset",),
    # path("password-reset/done/",
    #      PasswordResetDoneView.as_view(),
    #      name="password_reset_done",),
    # path("password-reset/<uidb64>/<token>/",
    #      PasswordResetConfirmView.as_view(),
    #      name="password_reset_confirm",),
    # path("password-reset/complete/",
    #      PasswordResetCompleteView.as_view(),
    #      name="password_reset_complete",),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]


