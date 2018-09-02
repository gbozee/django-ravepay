import json
import os
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from django.test import TestCase, override_settings
from django.shortcuts import reverse
from django.template import Context, Template
from ravepay.utils import RavepayAPI, load_lib
from django.conf import settings
# from django.utils.html import safe

@override_settings(DEBUG=True)
class RavepayTestCase(TestCase):

    def get_mock(self, mock_call, args):
        mock_instance = mock_call.return_value
        mock_instance.verify_payment.return_value = args
        return mock_instance

    @patch('ravepay.utils.RavepayAPI')
    def test_when_successful_redirects_to_default_success_url_when_not_set(self, mock_call):
        mock_instance = self.get_mock(
            mock_call, (
                True, "verification successful"))
        response = self.client.get(
            "{}?amount=30000&code=biola23".format(reverse('ravepay:verify_payment', args=['1234'])))
        mock_instance.verify_payment.assert_called_once_with(
            "biola23", 30000)
        self.assertEqual(response.url, reverse(
            'ravepay:successful_verification', args=['1234']))
        response = self.client.get(response.url)
        # import pdb; pdb.set_trace()
        self.assertEqual(response.url, reverse('ravepay:success_page'))

    @patch('ravepay.utils.RavepayAPI')
    def test_when_fails_redirects_to_default_fail_url_when_not_set(self, mock_call):
        mock_instance = self.get_mock(
            mock_call, (
                False, "failed transaction"))
        response = self.client.get(
            "{}?amount=30000&code=biola23".format(reverse('ravepay:verify_payment', args=['1234'])))
        mock_instance.verify_payment.assert_called_once_with(
            "biola23", 30000)
        self.assertEqual(response.url, reverse(
            'ravepay:failed_verification', args=['1234']))
        response = self.client.get(response.url)
        self.assertEqual(response.url, reverse('ravepay:failed_page'))

    @patch('ravepay.templatetags.ravepay.gen_hash')
    @patch('ravepay.templatetags.ravepay.get_random_string')
    def test_template_tag_renders_correctly(self, mock_random, mock_hash):
        mock_random.return_value = "a1234"
        mock_hash.return_value = "abcedesj"
        template_val = Template(
            """
        {% load ravepay %}
        {% ravepay_button button_class="red" amount=3000 email="gboze2@example.com" description="Buy Goods" %}
        """)
        context = Context({})
        template_response = template_val.render(context)
        self.assertIn('django-rave-button', template_response)
        val = {
            'customer_email':"gboze2@example.com",
            'customer_description':"Buy Goods",
            'custom_title': "Test Account",
            'amount': 3000,
            'country': "NG",
            'currency': 'NGN',
            'txtref': "A1234",
            'integrity_hash': "abcedesj",
            'PBFPubKey': settings.RAVEPAY_PUBLIC_KEY,
        }
        for rrr in val.values():
            self.assertIn(
               str(rrr), template_response)

    @patch('requests.post')
    def test_verify_payment_function_on_success(self, mock_post):
        mock_post.return_value = self.mock_request({
            "status": "success",
            "message": "Tx Fetched",
            "data": {
                "id": 5927,
                "tx_ref": "488-213",
                "order_ref": None,
                "flw_ref": "FLW-MOCK-f6c91bc6af09b183506287c8ebf81565",
                "transaction_type": "debit",
                "settlement_token": None,
                "transaction_processor": "FLW",
                "status": "successful",
                "chargeback_status": None,
                "ip": "93.119.198.5",
                "device_fingerprint": "fe9361090dbdd07b90170c14ebb3d8c5",
                "cycle": "one-time",
                "narration": "FLW-PBF CARD Transaction ",
                "amount": 27000,
                "appfee": 42.1875,
                "merchantfee": 0,
                "markupFee": None,
                "merchantbearsfee": 0,
                "charged_amount": 217.19,
                "transaction_currency": "NGN",
                "system_type": None,
                "payment_entity": "card",
                "payment_id": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-06-08T10:08:46.000Z",
                "updatedAt": "2017-06-08T10:08:50.000Z",
                "deletedAt": None,
                "merchant_id": 274,
                "addon_id": 3,
                "customer.id": 528,
                "customer.phone": None,
                "customer.fullName": "Anonymous customer",
                "customer.customertoken": None,
                "customer.email": "gaftonsifon@yandex.com",
                "customer.createdAt": "2017-06-05T13:51:47.000Z",
                "customer.updatedAt": "2017-06-05T13:51:47.000Z",
                "customer.deletedAt": None,
                "customer.AccountId": 274,
                "meta": [],
                "flwMeta": {
                    "chargeResponse": "00",
                    "chargeResponseMessage": "Success-Pending-otp-validation",
                    "VBVRESPONSEMESSAGE": "successful",
                    "VBVRESPONSECODE": "00",
                    "ACCOUNTVALIDATIONRESPMESSAGE": None,
                    "ACCOUNTVALIDATIONRESPONSECODE": None
                }
            }

        })
        instance = RavepayAPI()
        response = instance.verify_payment("12345", amount=27000)
        mock_post.assert_called_once_with(
            "{}/api/verify".format(instance.base_url),
            json={
                'flw_ref': "12345",
                "SECKEY": instance.secret_key,
                "normalize": "1"
            },
            headers={
                'content-type': "application/json"
            })
        self.assertTrue(response[0])
        self.assertEqual(response[1], "Verification Successful")

    @patch('requests.get')
    def test_verify_payment_function_on_fail(self, mock_post):
        mock_post.return_value = self.mock_request({
            "status": "error",
            "message": "No transaction found",
            "data": {
                "code": "NO TX",
                "message": "No transaction found"
            }
        }, status_code=400)
        instance = RavepayAPI()
        response = instance.verify_payment("12345", amount=27000)

        self.assertFalse(response[0])
        self.assertEqual(response[1], "Could not verify transaction")

    def mock_request(self, data, status_code=200):
        return MockRequst(data, status_code=status_code)


class NewTestCase(TestCase):

    @patch('requests.get')
    def test_can_load_external_module(self, mock_post):
        mock_post.return_value = MockRequst({
            "status": False,
            "message": "Invalid key"
        }, status_code=400)
        instance = load_lib('django_ravepay.mock_implement')()
        response = instance.verify_payment("12345", amount=27000)

        self.assertEqual(response, "hello")


class MockRequst(object):

    def __init__(self, response, **kwargs):
        self.response = response
        self.overwrite = True
        if kwargs.get('overwrite'):
            self.overwrite = True
        self.status_code = kwargs.get('status_code', 200)

    @classmethod
    def raise_for_status(cls):
        pass

    def json(self):
        if self.overwrite:
            return self.response
        return {'data': self.response}


# {'id': 236973, 'txRef': 'HVVHZ1YMSJIS', 'flwRef': 'FLW-MOCK-290b1f6a69a9be2bbb169ddacdafa142', 'orderRef': 'URF_1535879653950_3903335', 'paymentPlan': None, 'createdAt': '2018-09-02T09:14:13.000Z', 'amount': 100, 'charged_amount': 100, 'status': 'successful', 'IP': '197.210.65.21', 'currency': 'NGN', 'customer': {'id': 47452, 'phone': None, 'fullName': 'Anonymous
# customer', 'customertoken': None, 'email': 'gbozee@example.com', 'createdAt': '2018-09-02T09:14:13.000Z', 'updatedAt': '2018-09-02T09:14:13.000Z', 'deletedAt': None, 'AccountId': 7392}, 'entity': {'card6': '543889', 'card_last4': '0229'}, 'event.type': 'CARD_TRANSACTION'}

# {'id': 236975, 'txRef': 'HVVHZ1YMSJIS', 'flwRef': 'ACHG-1535880087754', 'orderRef': 'URF_1535880087003_7296735', 'paymentPlan': None, 'createdAt': '2018-09-02T09:21:27.000Z', 'amount': 100, 'charged_amount': 100, 'status': 'successful', 'IP': '197.210.65.21', 'currency': 'NGN', 'customer': {'id': 47453, 'phone': 'N/A', 'fullName': 'Anonymous customer', 'customertoken': None, 'email': 'gbozee@example.com', 'createdAt': '2018-09-02T09:21:26.000Z', 'updatedAt': '2018-09-02T09:21:26.000Z', 'deletedAt': None, 'AccountId': 7392}, 'entity': {'account_number': '0690000031', 'first_name': 'NO-NAME', 'last_name': 'NO-LNAME'}, 'event.type': 'ACCOUNT_TRANSACTION'}