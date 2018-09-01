import datetime
import hashlib
import json

from django import template
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from ravepay.utils import get_js_script
from .. import settings


def sign_request(raw):
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


register = template.Library()


def gen_hash(params):
    keys = sorted(params.keys())
    hashed_payload = (
        "".join([str(params[key]) for key in keys]) + settings.RAVEPAY_SECRET_KEY
    )
    return sign_request(hashed_payload)


def sorting(
    email="",
    first_name="",
    last_name="",
    description="",
    amount=200,
    phone="",
    country="",
    currency="",
    ref="",
):
    params = {
        "PBFPubKey": settings.RAVEPAY_PUBLIC_KEY,
        "customer_email": email,
        "customer_firstname": first_name,
        "customer_lastname": last_name,
        "custom_description": description,
        "custom_logo": settings.RAVEPAY_MODAL_LOGO,
        "custom_title": settings.RAVEPAY_MODAL_TITLE,
        "amount": amount,
        "customer_phone": phone,
        "country": country,
        "currency": currency,
        "txref": ref,
    }
    params = {key: value for key, value in params.items() if value}
    integrity_hash = gen_hash(params)
    new_params = params.copy()
    new_params.update(integrity_hash=integrity_hash)
    return new_params


@register.inclusion_tag("rave_button.html", takes_context=True)
def ravepay_button(
    context,
    button_id="django-rave-button",
    button_class="",
    phone=None,
    country="NG",
    currency="NGN",
    email=None,
    first_name=None,
    last_name=None,
    description=None,
    amount=None,
    ref=None,
    redirect_url=None,
):
    new_ref = ref
    new_redirect_url = redirect_url
    new_amount = int(amount)
    if not new_ref:
        new_ref = get_random_string().upper()
    if not new_redirect_url:
        new_redirect_url = "{}?amount={}".format(
            reverse("ravepay:verify_payment", args=[new_ref]), new_amount
        )
    params = sorting(
        email=email,
        first_name=first_name,
        last_name=last_name,
        description=description,
        amount=new_amount,
        phone=phone,
        country=country,
        currency=currency,
        ref=new_ref,
    )
    return {
        "js_url": get_js_script(False),
        "data": json.dumps(params),
        "button_id": button_id,
        "button_class": button_class,
        "redirect_url": new_redirect_url,
    }
