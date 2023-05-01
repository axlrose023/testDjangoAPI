import time
from datetime import timezone, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from restaurant.models import Menu
from user.models import User
from .models import Vote


def index(request):
    current_date = datetime.now(timezone.utc).date()
    menu = Menu.objects.filter(date=current_date)
    return render(request, 'index.html', {'menus': menu})


class EmployeeView(View):
    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            try:
                User.objects.create_employee(email=email, password=password)
                messages.success(request, 'Employee account created successfully!')
            except Exception as e:
                messages.error(request, f'Error creating employee account: {e}')
        else:
            messages.error(request, 'Email and password are required!')

        return redirect('index')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            print(user.is_employee)
            return redirect('index')

        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')


def vote(request, id):
    vot = Vote.objects.create(employee=request.user, menu_id=id)
    vot.save()
    return redirect('votes')


def votes(request):
    current_date = datetime.now(timezone.utc).date()
    votes = Vote.objects.filter(date=current_date)
    return render(request, 'votes.html', {'votes': votes})


class MenuView(View):
    def get(self, request):
        current_date = datetime.now(timezone.utc).date()
        menu = Menu.objects.filter(date=current_date)
        return render(request, 'current_menus.html', {'menus': menu})
