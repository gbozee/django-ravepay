import importlib

import requests

from . import settings
from django.conf import settings as dj_settings


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
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }
        url = "{}{}".format(self.base_url, path)
        headers = {
            'content-type': "application/json"
        }
        return options[method](url, headers=headers, **kwargs)

    def verify_result(self, response, **kwargs):
        result = response.json()
        if response.status_code == 200 and result['status'] == 'success':
            data = result['data']
            if data['amount'] == int(kwargs.get('amount')):
                return True, "Verification Successful"
            return False, data['amount']
        if response.status_code >= 400:
            return False, "Could not verify transaction"


    def verify_payment(self, code, amount):
        path = "/api/verify"
        response = self.make_request('POST', path, json={
            "flw_ref": code,
            "SECKEY": self.secret_key,
            "normalize": "1"
        })
        return self.verify_result(response,amount=amount)

def load_lib(config=settings.RAVEPAY_LIB_MODULE):
    module = importlib.import_module(config)
    return module.RavepayAPI
