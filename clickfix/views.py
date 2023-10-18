from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import *
from datetime import datetime, timedelta
from cart.models import *
from razorpayAPI.models import *
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .helper import *


def get_cart(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'])
    except:
        cart = None
    return cart


def home(request):
    services = Services.objects.all()
    testimonials = Testimonials.objects.all()

    cart = get_cart(request)
    deals = deals_and_discount.objects.all()
    data = {
        'services': services,
        'testimonials': testimonials,
        'cart': cart,
        'deals_and_discount': deals,
    }
    return render(request, 'home.html', data)


def individual_service(request, service_name, search_data=None):
    service = Services.objects.get(slug=service_name)
    sub_services = SubServices.objects.filter(service=service)
    deals = deals_and_discount.objects.all()
    cart = get_cart(request)

    date_list = []
    for i in range(7):
        date_list.append(datetime.today() + timedelta(days=i))

    data = {}
    data['sub_services'] = sub_services
    data['timeline'] = date_list
    data['cart'] = cart
    data['deals_and_discount'] = deals
    data['service'] = service

    if search_data:
        data['search_data'] = search_data

    return render(request, 'individual_service.html', data)


def checkout(request):
    if request.method == "POST":
        cart = get_cart(request)
        data = {}
        data['cart'] = cart
        data['grand_total'] = cart.get_cart_total()

        if cart.coupon:
            data['items_total'] = cart.get_cart_total() + cart.coupon.discount_price
        else:
            data['items_total'] = cart.get_cart_total()

        if request.user.is_authenticated:
            profile = Profile.objects.get(email=request.user.email)
            data['profile'] = profile

        return render(request, 'checkout.html', data)
    return HttpResponseBadRequest()


def live_tracking(request):
    data = {}
    if request.method == "POST":
        order_item_id = request.POST.get('order_item_id')
        order_item = OrderItem.objects.get(id=order_item_id)
        data['order_item'] = order_item
        cart = get_cart(request)
        data['cart'] = cart

        return render(request, 'live_tracking.html', data)

    return HttpResponseBadRequest()


def bookings(request):
    cart = get_cart(request)
    orders = []

    if request.user.is_authenticated:
        orders_by_logged_in_user = Order.objects.filter(user=request.user).order_by('-created_at')
        for order in orders_by_logged_in_user:
            orders.append(order)

    if 'nonuser' in request.session:
        orders_as_a_guest = Order.objects.filter(session_id=request.session['nonuser']).order_by('-created_at')
        for order in orders_as_a_guest:
            orders.append(order)

    order_items = []
    for item in orders:
        order_items += item.orderitems.all()

    data = {}
    data['cart'] = cart
    data['order_items'] = order_items

    return render(request, 'bookings.html', data)


def contact(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        client_email = request.POST.get('email')
        service_needed = request.POST.get('service_needed')
        phone_number = request.POST.get('phone')
        message = request.POST.get('message')
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



# def Order_SMS(request):
#     owner_whatsapp_number = ""
#     customer_whatsapp_number = ""

#     return HttpResponse("<h1> Success </h1>")
#     # SMS_Handler(owner_number=owner_whatsapp_number, customer_whatsapp_number=customer_whatsapp_number).send_message()


# def Order_Email(request):
#     customer_email = ""
#     customer_full_name = ""
#     Email_Handler(customer_email, customer_full_name).send_otp_via_mail()



def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        search_data = Services.objects.filter(Q(name__icontains=query))
        if search_data:
            service_name = search_data[0].slug
            return individual_service(request, service_name, search_data)
        else:
            messages.error(request, "Service Not Found!")
    return redirect('clickfix:home')


def book_rent_call(request):
    if request.method == "POST":
        product = request.POST.get('product')
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        quantity = request.POST.get('quantity')
        duration = request.POST.get('duration')
        description = request.POST.get('description')
        # service_slug = request.POST.get('service_slug')

        mail_subject = "Click Fix: You got a Call Booking For 'IT on Rent' Service"
        message = f"Full Name: {full_name}\nContact Number: {contact_number}\nQuantity: {quantity}\nDuration: {duration} days\nDescription: {description}"

        BookCall.objects.create(
            product=product,
            full_name = full_name,
            contact_number = contact_number,
            quantity = quantity,
            duration = duration,
            description = description,
            is_rent_call = True
        )

        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,
        )
        messages.success(request, "Your Call has been Booked, will get back to you soon")
    return redirect('clickfix:home')


def book_amc_call(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        description = request.POST.get('description')
        # service = Services.objects.get(slug=request.POST.get('service_slug'))

        mail_subject = "Click Fix: You got a Call Booking For 'AMC of IT assets' Service"
        message = f"Full Name: {full_name}\nContact Number: {contact_number}\nDescription: {description}"
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,
        )

        BookCall.objects.create(
            full_name = full_name,
            contact_number = contact_number,
            description = description,
            is_amc_call = True
        )
        messages.success(request, "Your Call has been Booked, will get back to you soon")
    return redirect('clickfix:home')
