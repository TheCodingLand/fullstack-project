
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
User = get_user_model()
from graphqlendpoint.models import Call

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('eventsmanager:user_list'))
        else:
            print(form.errors)
    return render(request, 'eventsmanager/log_in.html', {'form': form})

@login_required(login_url='/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('eventsmanager:log_in'))

def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('eventsmanager:log_in'))
        else:
            print(form.errors)
    return render(request, 'eventsmanager/sign_up.html', {'form': form})

@login_required(login_url='/log_in/')
def user_list(request):
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    return render(request, 'eventsmanager/user_list.html', {'users': users})


@login_required(login_url='/log_in/')
def user_list(request):
    calls = Call.objects.select_related('active')
    calls_list = []
    for call in calls:
        if hasattr(call, 'active'):
            calls_list.append(call)
    return render(request, 'eventsmanager/call_list.html', {'calls': calls_list}) 