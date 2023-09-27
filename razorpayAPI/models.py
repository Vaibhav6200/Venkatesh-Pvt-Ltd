from django.db import models
from cart.models import Cart, BillingDetails
from clickfix.models import *



class Order(models.Model):
    class Meta:
        verbose_name_plural = 'Orders'

    PAYMENT_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'))

    BOOKING_CHOICES = (
        ('Upcoming', 'Upcoming'),
        ('Rescheduled', 'Rescheduled'),
        ('Job Completed', 'Job Completed'),
        ('Booking Not Accepted', 'Booking Not Accepted'))

    TRACKING_CHOICES = (
        (1, 'Booked Today'),
        (2, 'Out For Service'),
        (3, 'Service Begun'),
        (4, 'Service Completed'))

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=10)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    billing_details = models.OneToOneField(BillingDetails, on_delete=models.CASCADE)
    total_cost = models.FloatField(default=0.0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    razorpay_order_id = models.CharField(max_length=100, default="")
    razorpay_payment_id = models.CharField(max_length=100, default="")
    booking_status = models.CharField(max_length=30, choices=BOOKING_CHOICES, null=True, blank=True)
    tracking_status = models.IntegerField(choices=TRACKING_CHOICES, null=True, blank=True)
    service_provider = models.ForeignKey(Handyman, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        if self.user:
            return f"Order #{self.id} by {self.user.username}"
        else:
            return f"Order #{self.id} by user with session_id = {self.session_id}"



class OrderItem(models.Model):
    class Meta:
        verbose_name_plural = 'Order Items'

    TIME_SLOTS = (
        ("10am-12pm", "10am-12pm"),
        ("12pm-2pm", "12pm-2pm"),
        ("2pm-4pm", "2pm-4pm"),
        ("4pm-7pm", "4pm-7pm"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    sub_service = models.ForeignKey(SubServices, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    start_date = models.DateField(null=True)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


