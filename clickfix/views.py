from django.shortcuts import render


def index(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def cart(request):
    return render(request, 'cart.html')

def individual_service(request):
    return render(request, 'individual_service.html')

def checkout(request):
    return render(request, 'checkout.html')

def live_tracking(request):
    return render(request, 'live_tracking.html')

def bookings(request):
    return render(request, 'bookings.html')