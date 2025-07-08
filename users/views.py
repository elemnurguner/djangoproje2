import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
# users/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('store:product_list')
    else:
        return redirect('store:product_list')  # GET ile gelirse de anasayfaya yönlendir


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, 'Lütfen “Ben robot değilim” kutusunu işaretleyin.')
        else:
            if form.is_valid():
                form.save()
                messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
                return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'form': form,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    })
