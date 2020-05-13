from .base import BaseClass
import logging
import base64
import hashlib

logger = logging.getLogger(__name__)

"""this is the getKey function that generates an encryption Key for you by passing your Secret Key as a parameter."""


def getKey(secret_key):
    hashedseckey = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
    hashedseckeylast12 = hashedseckey[-12:]
    seckeyadjusted = secret_key.replace("FLWSECK-", "")
    seckeyadjustedfirst12 = seckeyadjusted[:12]
    return seckeyadjustedfirst12 + hashedseckeylast12


"""This is the encryption function that encrypts your payload by passing the text and your encryption Key."""


def encryptData(key, plainText):
    from Crypto.Cipher import DES3

    blockSize = 8
    padDiff = blockSize - (len(plainText) % blockSize)
    cipher = DES3.new(key, DES3.MODE_ECB)
    plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
    encrypted = base64.b64encode(cipher.encrypt(plainText))
    return encrypted


class CardObject:
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key

    def build_card_object(self, currency="ngn", country="NG", **kwargs):
        obj = {
            "PBFPubKey": self.public_key,
            "currency": currency.upper(),
            "txref": kwargs["reference"],
            "country": country.upper(),
        }
        obj = update_obj(
            obj,
            kwargs,
            ["card_no", "cvv", "expiry_month", "expiry_year", "amount", "email"],
            required=True,
        )

        return {
            "phonenumber": "0902620185",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
            "txRef": "MC-" + Date.now(),
            "meta": [{metaname: "flightID", metavalue: "123949494DC"}],
            "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
        }


class Transaction(BaseClass):
    path = "/flwv3-pug/getpaidx"

    def verify_result(self, response, **kwargs):
        result = response.json()
        if response.status_code == 200 and result["status"] == "success":
            data = result["data"]
            logger.info("Amount from ravepay {}".format(data["amount"]))
            if float(data["amount"]) == float(kwargs.get("amount")):
                return True, "Verification Successful"
            return False, data["amount"]
        if response.status_code >= 400:
            return False, "Could not verify transaction"

    

    def verify_payment(self, code, amount_only=False, **kwargs):
        path = self.build_path("/api/v2/verify")
        response = self.make_request(
            "POST", path, json={"txref": code, "SECKEY": self.secret_key}
        )
        if amount_only:
            return self.verify_result(response, amount=kwargs.get("amount"))
        return self.result_format(response)

    def initialize_transaction(self, currency="ngn", **kwargs):
        """When we expect paystack to respond back to us once
        the payment is successful but not processing it
        from our end
        :params: kwargs{
            reference,
            email,
            amount, in naira.
            callback_url
        }
        """
        path = self.build_path("/api/v2/hosted/pay")
        json_data = {
            "txref": kwargs["reference"],
            "amount": float("%2f" % kwargs["amount"]),
            "redirect_url": kwargs["callback_url"],
            "currency": currency.upper(),
            "PBFPubKey": self.public_key,
        }
        json_data = update_obj(
            json_data,
            kwargs,
            ["first_name", "last_name", "phone", "email"],
            key="customer",
        )
        json_data = update_obj(
            json_data, kwargs, ["title", "description", "logo"], key="custom"
        )
        response = self.make_request("POST", path, json=json_data)

        return self.result_format(response)

    def build_transaction_obj(self,currency="ngn", **kwargs):
        json_data = {
            "txref": kwargs.get('reference') or kwargs.get('order'),
            "amount": float("%2f" % kwargs["amount"]),
            "redirect_url": kwargs["callback_url"],
            "currency": currency.upper(),
            "PBFPubKey": self.public_key,
        }
        json_data = update_obj(
            json_data,
            kwargs,
            ["first_name", "last_name", "phone", "email"],
            key="customer",
        )
        json_data = update_obj(
            json_data, kwargs, ["title", "description", "logo"], key="custom"
        )
        if kwargs.get('items'):
            json_data['meta'] = [{"metaname":x,"metavalue":y} for x,y in items.items()]
        return json_data


    def get_customer_and_auth_details(self, data):
        if data["status"] == "successful":
            customer = {
                "id": data.get("customerid"),
                "customer_email": data.get("custemail"),
                "customer_phonenumber": data.get("custphone"),
                "customer_fullname": data.get("custname"),
            }
            return {
                "account": data.get("account"),
                "authorization": data.get("card"),
                "customer": customer,
                "plan": data.get("paymentplan"),
            }
        return {}

    def recurrent_charge(self, currency="ngn", **kwargs):
        path = self.build_path("/api/tokenized/charge")
        json_data = {
            "SECKEY": self.secret_key,
            "token": kwargs["authorization_code"],
            "email": kwargs["email"],
            "amount": kwargs["amount"],
            "currency": currency.upper(),
        }
        if "order" in kwargs:
            json_data["txRef"] = kwargs["order"]
        response = self.make_request("POST", path, json=json_data)
        return self.result_format(response)

    def get_charge_token(self, data):
        if data["status"] == "successful":
            return data["chargeToken"]["embed_token"]

    def create_payment_account(self, account_name, email, is_permanent=True):
        path = "/v2/banktransfers/accountnumbers"
        json_data = {
            "seckey": self.secret_key,
            "email": email,
            "is_permanent": is_permanent,
            "narration": account_name,
        }
        response = self.make_request("POST", path, json=json_data)
        return self.result_format(response)

    def get_bank_info(self,data):
        return {
            "account_no": data['accountnumber'],
            'bank': data['bankname']
        }


def update_obj(old_data, kwargs, fields, key="", required=False):
    json_data = {**old_data}
    if required:
        assert set(list(kwargs.keys())).intersection(set(fields)) == set(fields)
    for key, value in kwargs.items():
        if key.lower() in fields:
            merge = key.replace("_", "").lower()
            key_obj = key
            if key:
                key_obj = "{}_{}".format(key, merge)
            json_data.update({key_obj: str(value)})
    return json_data
