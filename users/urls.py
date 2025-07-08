from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path
from .views import logout_view
from . import views
from .forms import CaptchaAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
   path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='users/login.html',
            authentication_form=CaptchaAuthenticationForm,
            extra_context={'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY}
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('logout/', logout_view, name='logout'),

]
