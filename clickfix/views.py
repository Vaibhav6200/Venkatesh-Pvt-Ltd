from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import *
from datetime import datetime, timedelta


def home(request):
    services = Services.objects.all()
    testimonials = Testimonials.objects.all()
    data = {
        'services': services,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', data)

def profile(request):
    return render(request, 'profile.html')

def individual_service(request, service_name):
    service = Services.objects.get(slug=service_name)
    sub_services = SubServices.objects.filter(service=service)

    week_days = []
    day_of_month = []
    for i in range(7):
        week_days.append((datetime.today() + timedelta(days=i)).strftime("%a"))
        day_of_month.append((datetime.today() + timedelta(days=i)).strftime("%d"))
    timeline = [(day, date) for day, date in zip(week_days, day_of_month)]

    data = {
        'sub_services': sub_services,
        'timeline': timeline,
    }
    return render(request, 'individual_service.html', data)

def checkout(request):
    return render(request, 'checkout.html')

def live_tracking(request):
    return render(request, 'live_tracking.html')

def bookings(request):
    return render(request, 'bookings.html')

def contact(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        client_email = request.POST.get('email')
        service_needed = request.POST.get('service_needed')
        phone_number = request.POST.get('phone')
        message = request.POST.get('query')
        mail_subject = f"ClickFix Query: from '{full_name}'"
        message += f"\n\nClient Email: {client_email}\nClient Phone: {phone_number}"
        to_email = settings.EMAIL_HOST_USER

        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
        Contact.objects.create(full_name=full_name, email=client_email,  service_needed=service_needed, mobile_number=phone_number, message=message)
        messages.success(request, "Your Query has been Recorded")
        return redirect('/')
    return render(request, 'contact.html')
