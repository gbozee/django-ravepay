import pytest
from ravepay.utils import RavepayAPI
from ravepay import utils


def test_verify_payment_failed(get_request, ravepay_api: utils.RavepayAPI):
    get_request({"status": False, "message": "Invalid key"}, status_code=400)
    response = ravepay_api.verify_payment("1234", amount=20000)
    assert not response[0]
    assert response[1] == "Could not verify transaction"


verify_payment_response = {
    "status": "success",
    "message": "Tx Fetched",
    "data": {
        "txid": 11399086,
        "txref": "UMWGR5P4RZ62",
        "flwref": "FLW067085553",
        "devicefingerprint": "f720d084fad44f99e3d6a065be5938d4",
        "cycle": "one-time",
        "amount": 100,
        "currency": "NGN",
        "chargedamount": 100,
        "appfee": 1.4,
        "merchantfee": 0,
        "merchantbearsfee": 1,
        "chargecode": "00",
        "chargemessage": "Kindly enter the OTP sent to *******9976 and g*******@gmail.com. OR enter the OTP generated on your Hardware Token device.",
        "authmodel": "GTB_OTP",
        "ip": "197.210.44.0",
        "narration": "CARD Transaction ",
        "status": "successful",
        "vbvcode": "00",
        "vbvmessage": "Approved",
        "authurl": "N/A",
        "acctcode": null,
        "acctmessage": null,
        "paymenttype": "card",
        "paymentid": "870866",
        "fraudstatus": "ok",
        "chargetype": "normal",
        "createdday": 6,
        "createddayname": "SATURDAY",
        "createdweek": 35,
        "createdmonth": 8,
        "createdmonthname": "SEPTEMBER",
        "createdquarter": 3,
        "createdyear": 2018,
        "createdyearisleap": false,
        "createddayispublicholiday": 0,
        "createdhour": 17,
        "createdminute": 54,
        "createdpmam": "pm",
        "created": "2018-09-01T17:54:42.000Z",
        "customerid": 4973390,
        "custphone": None,
        "custnetworkprovider": "N/A",
        "custname": "Anonymous customer",
        "custemail": "gbozee@example.com",
        "custemailprovider": "COMPANY EMAIL",
        "custcreated": "2018-09-01T17:54:42.000Z",
        "accountid": 3069,
        "acctbusinessname": "Tuteria",
        "acctcontactperson": "Biola Oyeniyi",
        "acctcountry": "NG",
        "acctbearsfeeattransactiontime": 1,
        "acctparent": 1,
        "acctvpcmerchant": "N/A",
        "acctalias": null,
        "acctisliveapproved": 0,
        "orderref": "URF_1535824482528_1476735",
        "paymentplan": null,
        "paymentpage": null,
        "raveref": "RV31535824481447A7354F6AD5",
        "amountsettledforthistransaction": 98.6,
        "card": {
            "expirymonth": "10",
            "expiryyear": "18",
            "cardBIN": "539983",
            "last4digits": "0569",
            "brand": "GUARANTY TRUST BANK Mastercard Naira Debit Card",
            "issuing_country": "NIGERIA NG",
            "card_tokens": [
                {"embedtoken": "   ", "shortcode": "eb33a", "expiry": "9999999999999"}
            ],
            "type": "MASTERCARD",
            "life_time_token": "   ",
        },
        "meta": [],
    },
}


def test_verify_payment_success(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    mock_post = post_request(side_effect=[verify_payment_response])
    result = ravepay_api.transaction_api.verify_payment("1234")
    mock_assertion(
        mock_post,
        "/flwv3-pug/getpaidx/api/v2/verify/",
        json={"txref": "1234", "SECKEY": ravepay_api.secret_key},
    )
    assert result[0]
    assert result[1] == "Verification successful"
    required_info = ravepay_api.transaction_api.get_customer_and_auth_details(result[2])
    assert required_info == {
        "authorization": {
            "expirymonth": "10",
            "expiryyear": "18",
            "cardBIN": "539983",
            "last4digits": "0569",
            "brand": "GUARANTY TRUST BANK Mastercard Naira Debit Card",
            "issuing_country": "NIGERIA NG",
            "card_tokens": [
                {"embedtoken": "   ", "shortcode": "eb33a", "expiry": "9999999999999"}
            ],
            "type": "MASTERCARD",
            "life_time_token": "flw-t1nf-6e6704a1164d2c85bf5b0a5f4792d599-k3n",
        },
        "customer": {
            "id": 4973390,
            "full_name": "Anonymous customer",
            "phone_no": None,
            "email": "gbozee@example.com",
        },
        "plan": None,
    }


def test_recurrent_charge_success_valid(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "Tx Fetched",
        "data": {
            "txid": 121257,
            "txref": "MC-1522438968515",
            "flwref": "FLW-MOCK-5e52517f0b314c73c56992dc620d8998",
            "devicefingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
            "cycle": "one-time",
            "amount": 10,
            "currency": "NGN",
            "chargedamount": 10,
            "appfee": 0,
            "merchantfee": 0,
            "merchantbearsfee": 1,
            "chargecode": "00",
            "chargemessage": "Charge successful. Please enter the OTP sent to your mobile number 080****** and email te**@rave**.com",
            "authmodel": "VBVSECURECODE",
            "ip": "::ffff:127.0.0.1",
            "narration": "FLW-PBF CARD Transaction ",
            "status": "successful",
            "vbvcode": "00",
            "vbvmessage": "successful",
            "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-5e52517f0b314c73c56992dc620d8998&code=00&message=Approved. Successful&receiptno=RN1522438999815",
            "acctcode": None,
            "acctmessage": None,
            "paymenttype": "card",
            "paymentid": "1057",
            "fraudstatus": "ok",
            "chargetype": "normal",
            "createdday": 5,
            "createddayname": "FRIDAY",
            "createdweek": 13,
            "createdmonth": 2,
            "createdmonthname": "MARCH",
            "createdquarter": 1,
            "createdyear": 2018,
            "createdyearisleap": None,
            "createddayispublicholiday": 0,
            "createdhour": 19,
            "createdminute": 43,
            "createdpmam": "pm",
            "created": "2018-03-30T19:43:19.000Z",
            "customerid": 21887,
            "custphone": "0902620185",
            "custnetworkprovider": "AIRTEL",
            "custname": "temi desola",
            "custemail": "desola.ade1@gmail.com",
            "custemailprovider": "GMAIL",
            "custcreated": "2018-03-30T19:43:19.000Z",
            "accountid": 134,
            "acctbusinessname": "Synergy Group",
            "acctcontactperson": "Desola Ade",
            "acctcountry": "NG",
            "acctbearsfeeattransactiontime": 1,
            "acctparent": 1,
            "acctvpcmerchant": "N/A",
            "acctalias": "temi",
            "acctisliveapproved": 0,
            "orderref": "URF_1522438999774_1285835",
            "paymentplan": None,
            "paymentpage": None,
            "raveref": "RV31522438998679C0566DED05",
            "amountsettledforthistransaction": 10,
            "card": {
                "expirymonth": "12",
                "expiryyear": "20",
                "cardBIN": "543889",
                "last4digits": "0229",
                "brand": "MASTERCARD MASHREQ BANK CREDITSTANDARD",
                "card_tokens": [
                    {
                        "embedtoken": "flw-t1nf-4877921998c0d784bbaf3949d23647a5-m03k",
                        "shortcode": "6a50e",
                        "expiry": "9999999999999",
                    }
                ],
                "life_time_token": "flw-t1nf-4877921998c0d784bbaf3949d23647a5-m03k",
            },
        },
    }
    mock_post = post_request(side_effect=[result])
    json_data = dict(
        embedtoken="AUTH_5z72ux0koz",
        email="bojack@horsinaround.com",
        amount=5000,
        order="123423232",
    )
    result = ravepay_api.transaction_api.recurrent_charge(**json_data)
    mock_assertion(
        mock_post,
        "/transaction/charge_authorization",
        json={
            "token": json_data["embedtoken"],
            "email": json_data["email"],
            "currency": "NGN",
            "txRef": "123423232",
            "amount": json_data["amount"] * 100,
            "SECKEY": ravepay_api.secret_key,
        },
    )
    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]
    assert response[2]["status"] == "successful"


def test_recurrent_charge_success_failed(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "error",
        "message": "Wrong token or email passed",
        "data": {
            "is_error": True,
            "code": "ERR",
            "message": "Wrong token or email passed",
        },
    }
    mock_post = post_request(result, status_code=400)
    json_data = dict(
        embedtoken="AUTH_5z72ux0koz",
        email="bojack@horsinaround.com",
        amount=5000,
        order="123423232",
    )
    result = ravepay_api.transaction_api.recurrent_charge(**json_data)
    assert not result[0]
    assert result[1] == "Wrong token or email passed"


def test_initialize_transaction_success(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": True,
        "message": "Authorization URL created",
        "data": {
            "authorization_url": "http://checkout.paystack.com/ravepay/7PVGX8MEk85tgeEpVDtD",
            "reference": "7PVGX8MEk85tgeEpVDtD",
        },
    }
    mock_post = post_request(result, status_code=400)
    json_data = {
        "reference": "7PVGX8MEk85tgeEpVDtD",
        "email": "james@example.com",
        "amount": 20000,
    }
    result = ravepay_api.transaction_api.initialize_transaction(**json_data)

    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]

