import importlib
import hmac
import hashlib
import requests

from . import settings
from django.conf import settings as dj_settings
import logging

logger = logging.getLogger(__name__)

def get_js_script():
    RAVEPAY_TEST_JS_LIB = (
        "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/flwpbf-inline.js"
    )
    RAVEPAY_LIVE_JS_LIB = (
        "https://api.ravepay.co/flwv3-pug/getpaidx/api/flwpbf-inline.js"
    )
    if dj_settings.DEBUG:
        return RAVEPAY_TEST_JS_LIB
    return RAVEPAY_LIVE_JS_LIB


class RavepayAPI(object):
    def __init__(self):
        self.public_key = settings.RAVEPAY_PUBLIC_KEY
        self.secret_key = settings.RAVEPAY_SECRET_KEY
        if dj_settings.DEBUG:
            self.base_url = settings.TEST_RAVEPAY_API_URL
        else:
            self.base_url = settings.RAVEPAY_API_URL

    def make_request(self, method, path, **kwargs):
        options = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
        }
        url = "{}{}".format(self.base_url, path)
        headers = {"content-type": "application/json"}
        return options[method](url, headers=headers, **kwargs)

    def verify_result(self, response, **kwargs):
        result = response.json()
        if response.status_code == 200 and result["status"] == "success":
            data = result["data"]
            logger.info("Amount from paystack {}".format(data["amount"]))
            if data["amount"] == float(kwargs.get("amount")):
                return True, "Verification Successful"
            return False, data["amount"]
        if response.status_code >= 400:
            return False, "Could not verify transaction"

    def verify_payment(self, code, amount):
        path = "/api/verify"
        response = self.make_request(
            "POST",
            path,
            json={"flw_ref": code, "SECKEY": self.secret_key, "normalize": "1"},
        )
        return self.verify_result(response, amount=amount)


def load_lib(config=settings.RAVEPAY_LIB_MODULE):
    module = importlib.import_module(config)
    return module.RavepayAPI


def generate_digest(data):
    return settings.RAVEPAY_WEBHOOK_HASH
    # return hmac.new(
    #     settings.RAVEPAY_SECRET_KEY.encode("utf-8"), msg=data, digestmod=hashlib.sha512
    # ).hexdigest()  # request body hash digest
