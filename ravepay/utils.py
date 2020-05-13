import importlib
import requests
from . import api
import logging

logger = logging.getLogger(__name__)


def get_js_script(is_debug=False):
    RAVEPAY_TEST_JS_LIB = (
        "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/flwpbf-inline.js"
    )
    RAVEPAY_LIVE_JS_LIB = (
        "https://api.ravepay.co/flwv3-pug/getpaidx/api/flwpbf-inline.js"
    )
    if is_debug:
        return RAVEPAY_TEST_JS_LIB
    return RAVEPAY_LIVE_JS_LIB


class RavepayAPI(object):
    TEST_URL = "https://ravesandboxapi.flutterwave.com"
    PRODUCTION_URL = "https://api.ravepay.co"
    WEBHOOK_HASH = "DJ_RAVEPAY"

    def __init__(self, django=True, test=False, webhook_hash=None, **kwargs):
        self.debug = test
        if django:
            from ravepay.frameworks.django import settings

            self.public_key = settings.RAVEPAY_PUBLIC_KEY
            self.secret_key = settings.RAVEPAY_SECRET_KEY
            if self.debug:
                self.base_url = settings.TEST_RAVEPAY_API_URL
            else:
                self.base_url = settings.RAVEPAY_API_URL
            self.webhook_hash = webhook_hash or settings.RAVEPAY_WEBHOOK_HASH
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)
            if self.debug:
                self.base_url = self.TEST_URL
            else:
                self.base_url = self.PRODUCTION_URL
            self.webhook_hash = webhook_hash or self.WEBHOOK_HASH
        self.transaction_api = api.Transaction(
            self.make_request, secret_key=self.secret_key, public_key=self.public_key
        )
        self.transfer_api = api.Transfer(
            self.make_request, secret_key=self.secret_key, public_key=self.public_key
        )
        self.webhook_api = api.Webhook(self.secret_key, self.webhook_hash)

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
        return self.transaction_api.verify_result(response, **kwargs)

    def verify_payment(self, code, **kwargs):
        return self.transaction_api.verify_payment(code, **kwargs)

    def generate_digest(self, data):
        return self.webhook_hash

    def processor_info(self, amount, redirect_url=None):
        return {
            "amount": float("%.2f" % amount),
            "js_script": get_js_script(is_debug=self.debug),
            "key": self.public_key,
            "redirect_url": redirect_url,
        }

    def other_payment_info(self, **kwargs):
        return self.transaction_api.build_transaction_obj(**kwargs)


def load_lib(config=None):
    from ravepay.frameworks.django import settings

    config_lib = config or settings.RAVEPAY_LIB_MODULE
    module = importlib.import_module(config)
    return module.RavepayAPI
