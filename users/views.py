from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from main.utils.get_user_score import get_user_score
from tests.models import Test
from .forms import RegistrationForm
from main.views import home_redirect
from django.conf import settings


def error_handler(request, exception):
    status_code = getattr(exception, 'status_code', 500)
    template_name = f"{status_code}.html"
    return render(request, template_name, status=status_code)


def profile(request):
    user = request.user
    context = {"user": user}

    return render(request, 'profile.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Регистрация успешно завершена.")
            return redirect('login')
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
            return redirect(home_redirect)
        else:
            messages.error(request, "Ошибка авторизации. Проверьте введенные данные.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def stats(request):
    user_score = get_user_score(request.user)
    context = {'user_score': user_score}
    return render(request, "stats.html", context)


def my_tests(request):
    tests = Test.objects.filter(author=request.user)

    context = {'tests': tests}

    return render(request, "my_tests.html", context)
