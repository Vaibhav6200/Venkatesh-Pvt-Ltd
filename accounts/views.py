from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from cart.models import Cart
from django.contrib import messages
from clickfix.models import Profile
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

# def login(request):
    # if request.user.is_authenticated:
    #     return redirect("/")

    # if request.method == "POST":
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         print(request.user.username)

    #         try:
    #             cart = Cart.objects.get(session_id=request.session['nonuser'], isPaid=False)
    #             if cart.objects.filter(user=request.user, isPaid=False).exists():
    #                 cart.user = None
    #                 cart.save()
    #             else:
    #                 cart.user = request.user
    #                 cart.save()
    #         except:
    #             print("we got an exception")

    #         return redirect('/')
    #     else:
    #         print("Invalid Credentials Provided")
    # data = {}
    # return render(request, 'login.html', data)




def register(request):
    # we have to check for 3 validations
    # (i) Password and confirmPassword should match
    # (ii) username id should be unique
    # (iii) email id should be unique
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
                user = Profile.objects.create(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
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
