from django.db import models
from .utils import generate_code
# Create your models here.


class RavePay(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    txref = models.CharField(
        max_length=12, primary_key=True, db_index=True)
    payment_method = models.CharField(
        max_length=30, default='both', choices=(
            ('both', 'both'),
            ('card', 'card'),
            ('account', 'account')
        )
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    country = models.CharField(max_length=5, default='NG')
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=15, blank=True)
    currency = models.CharField(max_length=10, default="NGN")
    verified = models.BooleanField(default=False)
    date_paid = models.DateTimeField(null=True)


    @classmethod
    def create(cls, **kwargs):
        order = generate_code(cls, 'ref')
        return cls(ref=order, **kwargs)
