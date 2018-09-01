from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from django.views.generic import RedirectView, TemplateView

from . import settings
from .signals import payment_verified
from .utils import load_lib


def verify_payment(request, order):
    amount = request.GET.get('amount')
    code = request.GET.get('code')
    RavepayAPI = load_lib()
    ravepay_instance = RavepayAPI()
    response = ravepay_instance.verify_payment(code, int(amount))
    if response[0]:
        payment_verified.send(
            sender=RavepayAPI, ref=order, amount=amount
        )
        return redirect(reverse('ravepay:successful_verification', args=[order]))
    return redirect(reverse('ravepay:failed_verification', args=[order]))


class FailedView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.RAVEPAY_FAILED_URL == 'ravepay:failed_page':
            return reverse(settings.RAVEPAY_FAILED_URL)
        return settings.RAVEPAY_FAILED_URL


class SuccessView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.RAVEPAY_SUCCESS_URL == 'ravepay:success_page':
            return reverse(settings.RAVEPAY_SUCCESS_URL)
        return settings.RAVEPAY_SUCCESS_URL
