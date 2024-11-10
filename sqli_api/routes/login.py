from sqli_api.forms import CustomLoginForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqli_api.models import CustomUser
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if not user.verified:
                messages.error(request, "Аккаунт не подтвержден! Дождитесь одобрения преподавателя.")
            else:
                if user is not None:
                    login(request, user)
                    return redirect('labs')
                else:
                    messages.error(request, 'Ошибка авторизации!')
        else:
            messages.error(request, 'Неверный логин или пароль!')
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            study_group = form.cleaned_data['study_group']
            password = form.cleaned_data['password1']

            CustomUser.objects.create_user(username=username,
                                           email=email,
                                           password=password,
                                           study_group=study_group)
            messages.success(request, "Ваш аккаунт успешно создан! Дождитесь подтверждения преподавателя.")
            return redirect('login')

        else:
            return render(request, 'accounts/register.html', {'form': form})

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')