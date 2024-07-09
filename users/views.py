from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm
from main.views import home_redirect
from django.conf import settings

def error_500_view(request, exception):
    return render(request, '500.html')

def error_410_view(request, exception):
    return render(request, '410.html')

def error_409_view(request, exception):
    return render(request, '409.html')

def error_404_view(request, exception):
    return render(request, '404.html')

def error_403_view(request, exception):
    return render(request, '403.html')

def error_401_view(request, exception):
    return render(request, '401.html')

def error_400_view(request, exception):
    return render(request, '400.html')

def error_304_view(request, exception):
    return render(request, '304.html')

def error_204_view(request, exception):
    return render(request, '204.html')

def error_201_view(request, exception):
    return render(request, '201.html')

def error_200_view(request, exception):
    return render(request, '200.html')



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
            return redirect(home_redirect)  # Перенаправьте на домашнюю страницу
        else:
            messages.error(request, "Ошибка авторизации. Проверьте введенные данные.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
