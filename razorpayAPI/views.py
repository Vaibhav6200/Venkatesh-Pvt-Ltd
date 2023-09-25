from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@csrf_exempt
def payment(request):
    if request.method == "POST":
        currency = "INR"
        amount = str(int(float(request.POST['amount'])) * 100)

        # creating razorpay order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://127.0.0.1:8000/razorpay/paymenthandler/'

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

        return render(request, 'razorpay/payment.html', context=context)
    return HttpResponseBadRequest()



@csrf_exempt
def paymenthandler(request):
    print("Reached to payment handler")
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
                    razorpay_client.payment.capture(payment_id, amount)     # capture the payemt
                    return render(request, 'paymentsuccess.html')       # render success page on successful caputre of payment
                except:
                    return render(request, 'paymentfail.html')      # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')      # if signature verification fails.
        except:
            return HttpResponseBadRequest()     # if we don't find the required parameters in POST data
    else:
        return HttpResponseBadRequest()     # if other than POST request is made.




def paymentsuccess(request):
    return render(request, 'razorpay/success.html')


def paymentfailure(request):
    return render(request, 'razorpay/failure.html')