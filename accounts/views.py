from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.messages import AppMessages
from .forms import CustomUserCreationForm, CustomUserChangeForm


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, AppMessages.ACCOUNT_CREATED)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('/admin')
            if user.role == 'agent':
                login(request, user)
                messages.success(request, AppMessages.LOGIN_SUCCESS)
                return redirect('/tickets/dashboard')
            login(request, user)
            messages.success(request, AppMessages.LOGIN_SUCCESS)
            return redirect('ticket_list')
        else:
            messages.error(request, AppMessages.LOGIN_FAILED)
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, AppMessages.ELEMENT_UPDATED)
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})
