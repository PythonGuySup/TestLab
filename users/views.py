from django.shortcuts import render, redirect
from django.contrib.auth import login
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
            return redirect(home_redirect)
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(home_redirect)