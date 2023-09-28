from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from cart.models import *



def get_cart(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'])
    except:
        cart = {'num_of_items': 0}
    return cart


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


def profile(request):
    if request.user.is_authenticated:
        data = {}
        profile = Profile.objects.get(email=request.user.email)
        if request.method == "POST":
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            email = request.POST.get('email', None)
            phone = request.POST.get('phone', None)
            dob = request.POST.get('dob', None)
            billing_address = request.POST.get('billing_address', None)
            bio = request.POST.get('bio')
            new_password = request.POST.get('new_password', None)
            confirm_new_password = request.POST.get('confirm_new_password', None)
            profile_image = request.FILES.get('profile_image', None)

            if profile_image:
                profile.image = profile_image
            if first_name:
                profile.first_name = first_name
            if last_name:
                profile.last_name = last_name
            if email:
                profile.email = email
            if phone:
                profile.phone = phone
            if dob:
                profile.dob = dob
            if billing_address:
                profile.billing_address = billing_address
            if bio:
                profile.bio = bio
            if new_password and confirm_new_password and new_password == confirm_new_password:
                profile.set_password(new_password)
            profile.save()

        data['profile'] = profile
        data['cart'] = get_cart(request)
        return render(request, 'profile.html', data)
    return HttpResponseBadRequest()
