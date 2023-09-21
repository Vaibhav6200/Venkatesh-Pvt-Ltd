from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from cart.models import Cart


def register(request):
    if request.user.is_authenticated:
        return render(request, "home.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(request.user.username)

            try:
                cart = Cart.objects.get(session_id=request.session['nonuser'], isPaid=False)
                if cart.objects.filter(user=request.user, isPaid=False).exists():
                    cart.user = None
                    cart.save()
                else:
                    cart.user = request.user
                    cart.save()
            except:
                print("we got an exception")

            return redirect('/')
        else:
            print("Invalid Credentials Provided")
    data = {}
    return render(request, 'login.html', data)
