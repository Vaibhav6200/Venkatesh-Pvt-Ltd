from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.http import HttpResponseRedirect



def register(request):
    if request.user.is_authenticated:
        return render(request, "home.html")

# Create your views here.
def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        login_password = request.POST['password']
        user = authenticate(email=email, password=login_password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("accounts:login")
    return render(request, 'accounts/login.html')


def register(request):
    if request.method == "POST":
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['cpassword']

        if password == confirm_password:
            if Profile.objects.filter(username=username).exists():
                messages.error(request, "username already exists")
                return redirect('accounts:register')
            else:
                user = Profile(first_name=firstname, last_name=lastname, username=username, email=email)
                user.set_password(password)
                user.save()
                login(request, user)
                user.save()
                messages.success(request, "You are Successfully Registered!")
                return redirect("/")
        else:
            messages.error(request, "Passwords do not match")
            return HttpResponseRedirect(request.path_info)  # redirect to same page
    return render(request, 'accounts/register.html')


def user_logout(request):
    logout(request)
    return redirect("/")
