from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'accounts/register.html',
                {'error': 'Ce nom d’utilisateur existe déjà'}
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('home')

    return render(request, 'accounts/register.html')


def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'accounts/login.html',
            {'error': 'Nom d’utilisateur ou mot de passe incorrect'}
        )

    return render(request, 'accounts/login.html')



