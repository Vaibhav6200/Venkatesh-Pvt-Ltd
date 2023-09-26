from cart.models import Cart, CartItem
from razorpayAPI.models import Order


def handle_order(request, razorpay_order_id, payment_id):

    order_obj = Order.objects.get(razorpay_order_id=razorpay_order_id)
    order_obj.razorpay_payment_id = payment_id
    order_obj.payment_status = "Paid"

    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get(user=user)
    else:
        session_id = request.session['nonuser']
        cart = Cart.objects.get(session_id=session_id)

    # We Got Our cart Here So we will Now Move All of our Cart Items to our orderitem
    order_obj.save()
