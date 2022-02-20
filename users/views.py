from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def register_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        message = False
        if User.objects.filter(username=username).exists():
            message = 'There is already an user with that username'
        if User.objects.filter(email=email).exists():
            message = 'There is already an user with that email'
        if len(username) < 3:
            message = 'Username must be at least 3 characters long'
        if len(username) >= 30:
            message = 'Username must be less than 30 characters long'
        if len(password) < 4:
            message = 'Password must be at least 4 characters long'
        if message:
            context = {'message': message}
            return render(request, 'registration_form.html', context)
        try:
            User.objects.create_user(username=username, email=email, password=password,
                                     first_name=first_name, last_name=last_name)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        except:
            message = 'Something went wrong'
            context = {'message': message}
            return render(request, 'registration_form.html', context)
    else:
        return render(request, 'registration_form.html')


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            message = 'Invalid username or password'
            context = {'message': message}
            return render(request, 'login_form.html', context)
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'login_form.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request, message=None):
    user = request.user
    return render(request, 'profile.html', {'user': user, 'message': message})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user = User.objects.get(id=user.id)
        data = request.POST
        if len(data.get('email')) > 0 and User.objects.filter(email=data.get('email')).exists() and User.objects.filter(
                email=data.get('email')).first().id != user.id:
            message = 'There is already an user with that email'
            return render(request, 'edit_profile.html', {'message': message, 'user': user})
        user.email = data.get('email') if data.get('email') else user.email
        user.first_name = data.get('first_name') if data.get('first_name') else user.first_name
        user.last_name = data.get('last_name') if data.get('last_name') else user.last_name
        user.save()
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        return render(request, 'edit_profile.html', {'user': user})


@login_required
def change_password(request):
    if request.method == 'POST':
        data = request.POST
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')
        user = request.user
        message = False
        if not user.check_password(old_password):
            message = 'Old password is incorrect'
        if new_password != new_password_confirm:
            message = 'New passwords do not match'
        if message:
            return render(request, 'change_password.html', {'message': message})
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect(reverse('users:profile'), {'message': 'Password changed'})
    else:
        return render(request, 'change_password.html')


@login_required
def deactivate_account(request):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    return HttpResponseRedirect(reverse('home'))
