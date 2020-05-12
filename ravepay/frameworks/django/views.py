from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from django.views.generic import RedirectView, TemplateView
import json
from django.http import JsonResponse
from . import settings
from ravepay import utils
from ravepay.api import signals
from ravepay.api.signals import payment_verified
from ravepay.utils import load_lib


def verify_payment(request, order):
    amount = request.GET.get("amount")
    code = request.GET.get("code")
    RavepayAPI = load_lib()
    ravepay_instance = RavepayAPI()
    response = ravepay_instance.verify_payment(code, float(amount))
    if response[0]:
        payment_verified.send(sender=RavepayAPI, ref=order, amount=amount)
        return redirect(reverse("ravepay:successful_verification", args=[order]))
    return redirect(reverse("ravepay:failed_verification", args=[order]))


def success_redirect_view(request, order_id):
    url = settings.RAVEPAY_SUCCESS_URL
    if url == "ravepay:success_page":
        url = reverse(url)
    return redirect(url, permanent=True)


def failure_redirect_view(request, order_id):
    url = settings.RAVEPAY_FAILED_URL
    if url == "ravepay:failed_page":
        url = reverse(url)
    return redirect(url, permanent=True)


class FailedView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.RAVEPAY_FAILED_URL == "ravepay:failed_page":
            return reverse(settings.RAVEPAY_FAILED_URL)
        return settings.RAVEPAY_FAILED_URL


class SuccessView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.RAVEPAY_SUCCESS_URL == "ravepay:success_page":
            return reverse(settings.RAVEPAY_SUCCESS_URL)
        return settings.RAVEPAY_SUCCESS_URL


def webhook_view(request):
    # ensure that all parameters are in the bytes representation
    RavepayAPI = load_lib()
    ravepay_instance = RavepayAPI()
    signature = request.META["HTTP_VERIF_HASH"]
    ravepay_instance.webhook_api.verify(signature, request.body, full_auth=True)
    # digest = utils.generate_digest(request.body)
    # if digest == signature:
    #     payload = json.loads(request.body)
    #     signals.event_signal.send(
    #         sender=request, event=payload["event.type"], data=payload
    #     )
    return JsonResponse({"status": "Success"})
