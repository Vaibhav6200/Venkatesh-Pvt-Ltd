from django.db import models


class Coupon(models.Model):
    image = models.ImageField(upload_to='coupon_images', null=True, blank=True)
    coupon_code = models.CharField(max_length=20, help_text="max length of coupon can be 20 characters")
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField()
    minimum_price = models.IntegerField()

    def __str__(self):
        return self.coupon_code