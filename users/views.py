from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm
from main.views import home_redirect


def profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Регистрация успешно завершена.")
            return redirect('login.html')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(home_redirect)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(home_redirect)  # Перенаправьте на домашнюю страницу
        else:
            messages.error(request, "Ошибка авторизации. Проверьте введенные данные.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
