from django.shortcuts import render, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Order
from cart.models import Cart
# from urllib.parse import urlparse



KEY_ID = settings.RAZORPAY_KEY_ID
KEY_SECRET = settings.RAZORPAY_KEY_SECRET

razorpay_client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

@csrf_exempt
def payment(request):
    if request.method == "POST":
        currency = "INR"
        amount = str(int(float(request.POST['amount'])) * 100)

        # creating razorpay order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        order_obj = Order.objects.get(id=request.POST['order_id'])
        order_obj.razorpay_order_id = razorpay_order_id
        order_obj.save()

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = 'http://127.0.0.1:8000/razorpay/paymenthandler/'
        # context['callback_url'] = "http://john001.pythonanywhere.com/razorpay/paymenthandler/"

        return render(request, 'razorpay/payment.html', context=context)
    return HttpResponseBadRequest()



@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                order = razorpay_client.order.fetch(razorpay_order_id)
                amount = order['amount']
                try:
                    print("Payment Capture Successfull")
                    razorpay_client.payment.capture(payment_id, amount)     # capture the payemt
                    order_obj = Order.objects.get(razorpay_order_id=razorpay_order_id)
                    order_obj.razorpay_payment_id = payment_id
                    order_obj.payment_status = "Paid"
                    order_obj.booking_status = "Upcoming"
                    order_obj.tracking_status = 1
                    order_obj.save()

                    # Since Order Placed Successfully So remove all items from our cart
                    cart_id = order_obj.cart_id
                    Cart.objects.get(id=cart_id).delete()

                    return redirect('clickfix:bookings')       # render success page on successful caputre of payment
                except:
                    print("Error in Payment Capture")
                    order_obj = Order.objects.get(razorpay_order_id=razorpay_order_id)
                    order_obj.razorpay_payment_id = payment_id
                    order_obj.payment_status = "Failed"
                    order_obj.save()
                    return redirect('razorpay:paymentfail')      # if there is an error while capturing payment.
            else:
                print("Signature NOT Verified")
                return redirect('razorpay:paymentfail')      # if signature verification fails.
        except:
            print("Getting HTTP bad request error from here")
            return HttpResponseBadRequest()     # if we don't find the required parameters in POST data
    else:
        return HttpResponseBadRequest()     # if other than POST request is made.




def paymentsuccess(request):
    return render(request, 'razorpay/success.html')


def paymentfailure(request):
    return render(request, 'razorpay/failure.html')