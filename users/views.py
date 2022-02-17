from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


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
        if len(username) <= 3:
            message = 'Username must be at least 3 characters long'
        if len(username) >= 30:
            message = 'Username must be less than 30 characters long'
        if len(password) <= 4:
            message = 'Password must be at least 4 characters long'
        if message:
            context = {'message': message}
            return render(request, 'registration_form.html', context)
        try:
            User.objects.create_user(username=username, email=email, password=password,
                                     first_name=first_name, last_name=last_name)
            authenticate(request, username=username, password=password)
            return HttpResponse('User registered')
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
        return HttpResponseRedirect('/')
    else:
        return render(request, 'login_form.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
