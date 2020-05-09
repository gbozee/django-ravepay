import pytest
from ravepay.utils import RavepayAPI
from ravepay import utils


def test_verify_payment_failed(get_request, ravepay_api: utils.RavepayAPI):
    get_request({"status": False, "message": "Invalid key"}, status_code=400)
    response = ravepay_api.verify_payment("1234", amount_only=True, amount=20000)
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
        "acctcode": None,
        "acctmessage": None,
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
        "createdyearisleap": False,
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
        "acctalias": None,
        "acctisliveapproved": 0,
        "orderref": "URF_1535824482528_1476735",
        "paymentplan": None,
        "paymentpage": None,
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

card_transaction_response = {
    "status": "success",
    "message": "Tx Fetched",
    "data": {
        "txid": 157906,
        "txref": "Rave-Pages247523551187",
        "flwref": "FLW-MOCK-2c72cec359fd4ea1ee6f188b364726ad",
        "devicefingerprint": "532b4e9fa7695279392f4780b9868b9b",
        "cycle": "one-time",
        "amount": 700,
        "currency": "NGN",
        "chargedamount": 700,
        "appfee": 0,
        "merchantfee": 0,
        "merchantbearsfee": 1,
        "chargecode": "00",
        "chargemessage": "Please enter the OTP sent to your mobile number 080****** and email te**@rave**.com",
        "authmodel": "AVS_VBVSECURECODE",
        "ip": "197.149.95.62",
        "narration": "CARD Transaction ",
        "status": "successful",
        "vbvcode": "00",
        "vbvmessage": "Approved. Successful",
        "authurl": "https://ravesandboxapi.flutterwave.com/mockvbvpage?ref=FLW-MOCK-2c72cec359fd4ea1ee6f188b364726ad&cod ...",
        "acctcode": "RN1527618494727",
        "acctmessage": None,
        "paymenttype": "card",
        "paymentid": "915",
        "fraudstatus": "ok",
        "chargetype": "normal",
        "createdday": 2,
        "createddayname": "TUESDAY",
        "createdweek": 22,
        "createdmonth": 4,
        "createdmonthname": "MAY",
        "createdquarter": 2,
        "createdyear": 2018,
        "createdyearisleap": False,
        "createddayispublicholiday": 0,
        "createdhour": 18,
        "createdminute": 28,
        "createdpmam": "pm",
        "created": "2018-05-29T18:28:14.000Z",
        "customerid": 29457,
        "custphone": None,
        "custnetworkprovider": "N/A",
        "custname": "Temi Adesina",
        "custemail": "temiloluwa_adesina@yahoo.com",
        "custemailprovider": "YAHOO",
        "custcreated": "2018-05-29T18:28:13.000Z",
        "accountid": 134,
        "acctbusinessname": "Synergy Group",
        "acctcontactperson": "Desola Ade",
        "acctcountry": "NG",
        "acctbearsfeeattransactiontime": 1,
        "acctparent": 1,
        "acctvpcmerchant": "N/A",
        "acctalias": "temi",
        "acctisliveapproved": 0,
        "orderref": "URF_1527618494622_833935",
        "paymentplan": None,
        "paymentpage": 681,
        "raveref": "RV315276184933313A412EE9C1",
        "amountsettledforthistransaction": 700,
        "card": {
            "expirymonth": "01",
            "expiryyear": "19",
            "cardBIN": "455605",
            "last4digits": "2643",
            "brand": " CREDIT",
            "card_tokens": [
                {
                    "embedtoken": "flw-t1nf-ad7bc612ce74edf8ef2d348fa83ee2c9-m03k",
                    "shortcode": "89b11",
                    "expiry": "9999999999999",
                }
            ],
            "type": "VISA",
            "life_time_token": "flw-t1nf-ad7bc612ce74edf8ef2d348fa83ee2c9-m03k",
        },
        "meta": [
            {
                "id": 30117,
                "metaname": "Book ID",
                "metavalue": "jsjsjsjs",
                "createdAt": "2018-05-29T18:28:16.000Z",
                "updatedAt": "2018-05-29T18:28:16.000Z",
                "deletedAt": None,
                "getpaidTransactionId": 157906,
            },
            {
                "id": 30118,
                "metaname": "actual_charge_amount",
                "metavalue": "700.00",
                "createdAt": "2018-05-29T18:28:16.000Z",
                "updatedAt": "2018-05-29T18:28:16.000Z",
                "deletedAt": None,
                "getpaidTransactionId": 157906,
            },
            {
                "id": 30119,
                "metaname": "converted_amount",
                "metavalue": "2.02",
                "createdAt": "2018-05-29T18:28:16.000Z",
                "updatedAt": "2018-05-29T18:28:16.000Z",
                "deletedAt": None,
                "getpaidTransactionId": 157906,
            },
        ],
    },
}

account_transaction_response = {
    "status": "success",
    "message": "Tx Fetched",
    "data": {
        "txid": 157524,
        "txref": "Rave-Pages655350753556",
        "flwref": "FLWACHMOCK-1527583529027",
        "devicefingerprint": "532b4e9fa7695279392f4780b9868b9b",
        "cycle": "one-time",
        "amount": 700,
        "currency": "NGN",
        "chargedamount": 700,
        "appfee": 0,
        "merchantfee": 0,
        "merchantbearsfee": 1,
        "chargecode": "00",
        "chargemessage": "Approved. Successful.",
        "authmodel": "AUTH",
        "ip": "41.190.30.27",
        "narration": "Synergy Group",
        "status": "successful",
        "vbvcode": "N/A",
        "vbvmessage": "N/A",
        "authurl": "NO-URL",
        "acctcode": None,
        "acctmessage": None,
        "paymenttype": "account",
        "paymentid": "478",
        "fraudstatus": "ok",
        "chargetype": "normal",
        "createdday": 2,
        "createddayname": "TUESDAY",
        "createdweek": 22,
        "createdmonth": 4,
        "createdmonthname": "MAY",
        "createdquarter": 2,
        "createdyear": 2018,
        "createdyearisleap": False,
        "createddayispublicholiday": 0,
        "createdhour": 8,
        "createdminute": 45,
        "createdpmam": "am",
        "created": "2018-05-29T08:45:26.000Z",
        "customerid": 29378,
        "custphone": "N/A",
        "custnetworkprovider": "UNKNOWN PROVIDER",
        "custname": "Temi Adesina",
        "custemail": "temiloluwa_adesina@yahoo.com",
        "custemailprovider": "YAHOO",
        "custcreated": "2018-05-29T08:45:26.000Z",
        "accountid": 134,
        "acctbusinessname": "Synergy Group",
        "acctcontactperson": "Desola Ade",
        "acctcountry": "NG",
        "acctbearsfeeattransactiontime": 1,
        "acctparent": 1,
        "acctvpcmerchant": "N/A",
        "acctalias": "temi",
        "acctisliveapproved": 0,
        "orderref": "URF_1527583526904_2107135",
        "paymentplan": None,
        "paymentpage": None,
        "raveref": "RV315275835263042C559EA650",
        "amountsettledforthistransaction": 700,
        "account": {
            "id": 478,
            "account_number": "0690000037",
            "account_bank": "044",
            "first_name": "Dele Moruf",
            "last_name": "Quadri",
            "account_is_blacklisted": 0,
            "createdAt": "2018-04-05T13:30:04.000Z",
            "updatedAt": "2018-06-01T06:03:41.000Z",
            "deletedAt": None,
            "account_token": {"token": "flw-t0cd8f7ac849807c50-k3n-mock"},
        },
        "meta": [
            {
                "id": 30106,
                "metaname": "Book ID",
                "metavalue": "hsjsjsj",
                "createdAt": "2018-05-29T08:45:26.000Z",
                "updatedAt": "2018-05-29T08:45:26.000Z",
                "deletedAt": None,
                "getpaidTransactionId": 157524,
            }
        ],
    },
}


def test_card_payment_success(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    mock_post = post_request(side_effect=[card_transaction_response])
    result = ravepay_api.transaction_api.verify_payment("1234")
    mock_assertion(
        mock_post,
        "/flwv3-pug/getpaidx/api/v2/verify",
        json={"txref": "1234", "SECKEY": ravepay_api.secret_key},
    )
    assert result[0]
    assert result[1] == "Tx Fetched"
    required_info = ravepay_api.transaction_api.get_customer_and_auth_details(result[2])
    assert required_info == {
        "authorization": {
            "expirymonth": "01",
            "expiryyear": "19",
            "cardBIN": "455605",
            "last4digits": "2643",
            "brand": " CREDIT",
            "card_tokens": [
                {
                    "embedtoken": "flw-t1nf-ad7bc612ce74edf8ef2d348fa83ee2c9-m03k",
                    "shortcode": "89b11",
                    "expiry": "9999999999999",
                }
            ],
            "type": "VISA",
            "life_time_token": "flw-t1nf-ad7bc612ce74edf8ef2d348fa83ee2c9-m03k",
        },
        "account": None,
        "customer": {
            "id": 29457,
            "customer_email": "temiloluwa_adesina@yahoo.com",
            "customer_phonenumber": None,
            "customer_fullname": "Temi Adesina",
        },
        "plan": None,
    }


def test_card_payment_success_amount(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    mock_post = post_request(side_effect=[card_transaction_response])
    result = ravepay_api.transaction_api.verify_payment(
        "1234", amount_only=True, amount="700"
    )
    mock_assertion(
        mock_post,
        "/flwv3-pug/getpaidx/api/v2/verify",
        json={"txref": "1234", "SECKEY": ravepay_api.secret_key},
    )
    assert result[0]
    assert result[1] == "Verification Successful"


def test_card_payment_failed_amount(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    mock_post = post_request(side_effect=[card_transaction_response])
    result = ravepay_api.transaction_api.verify_payment(
        "1234", amount_only=True, amount="400"
    )
    mock_assertion(
        mock_post,
        "/flwv3-pug/getpaidx/api/v2/verify",
        json={"txref": "1234", "SECKEY": ravepay_api.secret_key},
    )
    assert not result[0]
    assert result[1] == 700


def test_account_payment_success(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    mock_post = post_request(side_effect=[account_transaction_response])
    result = ravepay_api.transaction_api.verify_payment("1234")
    mock_assertion(
        mock_post,
        "/flwv3-pug/getpaidx/api/v2/verify",
        json={"txref": "1234", "SECKEY": ravepay_api.secret_key},
    )
    assert result[0]
    assert result[1] == "Tx Fetched"
    required_info = ravepay_api.transaction_api.get_customer_and_auth_details(result[2])
    assert required_info == {
        "authorization": None,
        "account": {
            "id": 478,
            "account_number": "0690000037",
            "account_bank": "044",
            "first_name": "Dele Moruf",
            "last_name": "Quadri",
            "account_is_blacklisted": 0,
            "createdAt": "2018-04-05T13:30:04.000Z",
            "updatedAt": "2018-06-01T06:03:41.000Z",
            "deletedAt": None,
            "account_token": {"token": "flw-t0cd8f7ac849807c50-k3n-mock"},
        },
        "customer": {
            "id": 29378,
            "customer_email": "temiloluwa_adesina@yahoo.com",
            "customer_phonenumber": "N/A",
            "customer_fullname": "Temi Adesina",
        },
        "plan": None,
    }


def test_recurrent_charge_success_valid(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "Charge success",
        "data": {
            "id": 1271960,
            "txRef": "23244232",
            "orderRef": "URF_8D76FD96F96BCDF6EE_7004334",
            "flwRef": "FLW-M03K-59cef0904589df3e641898fe94f932fe",
            "redirectUrl": "http://127.0.0",
            "device_fingerprint": "N/A",
            "settlement_token": None,
            "cycle": "one-time",
            "amount": 25.25,
            "charged_amount": 25.25,
            "appfee": 0.71,
            "merchantfee": 0,
            "merchantbearsfee": 1,
            "chargeResponseCode": "00",
            "raveRef": None,
            "chargeResponseMessage": "Approved",
            "authModelUsed": "noauth",
            "currency": "NGN",
            "IP": "::127.0.0.1",
            "narration": "Tuteria",
            "status": "successful",
            "modalauditid": "9798b8d3b1a5969db657db8a6e57cc52",
            "vbvrespmessage": "Approved",
            "authurl": "N/A",
            "vbvrespcode": "00",
            "acctvalrespmsg": None,
            "acctvalrespcode": None,
            "paymentType": "card",
            "paymentPlan": None,
            "paymentPage": None,
            "paymentId": "6490",
            "fraud_status": "ok",
            "charge_type": "normal",
            "is_live": 0,
            "retry_attempt": None,
            "getpaidBatchId": None,
            "createdAt": "2020-05-08T19:43:24.000Z",
            "updatedAt": "2020-05-08T19:43:24.000Z",
            "deletedAt": None,
            "customerId": 376992,
            "AccountId": 24349,
            "customer": {
                "id": 376992,
                "phone": None,
                "fullName": "Abiola Oyeniyi",
                "customertoken": None,
                "email": "gbozee@gmail.com",
                "createdAt": "2020-05-08T08:19:11.000Z",
                "updatedAt": "2020-05-08T08:19:11.000Z",
                "deletedAt": None,
                "AccountId": 24349,
            },
            "chargeToken": {
                "user_token": "4ba9d",
                "embed_token": "flw-t0-f507df230d6becc7f2953eebef808171-m03k",
            },
        },
    }
    mock_post = post_request(side_effect=[result])
    json_data = dict(
        authorization_code="AUTH_5z72ux0koz",
        email="bojack@horsinaround.com",
        amount=5000,
        order="123423232",
    )
    response = ravepay_api.transaction_api.recurrent_charge(**json_data)
    mock_assertion(
        mock_post,
        "/flwv3-pug/getpaidx/api/tokenized/charge",
        json={
            "token": json_data["authorization_code"],
            "email": json_data["email"],
            "currency": "NGN",
            "txRef": "123423232",
            "amount": json_data["amount"],
            "SECKEY": ravepay_api.secret_key,
        },
    )
    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]
    assert response[2]["status"] == "successful"
    required_info = ravepay_api.transaction_api.get_charge_token(response[2])
    assert required_info == "flw-t0-f507df230d6becc7f2953eebef808171-m03k"


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
        authorization_code="AUTH_5z72ux0koz",
        email="bojack@horsinaround.com",
        amount=5000,
        order="123423232",
    )
    response = ravepay_api.transaction_api.recurrent_charge(**json_data)
    assert not response[0]
    assert response[1] == "Wrong token or email passed"


def test_payment_account_creation(
    mock_assertion, post_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "BANKTRANSFERS-ACCOUNTNUMBER-CREATED",
        "data": {
            "response_code": "02",
            "response_message": "Transaction in progress",
            "orderRef": "URF_1588969680068_3810335",
            "accountnumber": "1234567890",
            "bankname": "TEST BANK",
            "amount": None,
        },
    }
    mock_post = post_request(result, status_code=200)
    response = ravepay_api.transaction_api.create_payment_account(
        "Tuteria Limited", "james@example.com"
    )
    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]
    bank_info = ravepay_api.transaction_api.get_bank_info(response[2])
    assert bank_info == {"account_no": "1234567890", "bank": "TEST BANK"}


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
    mock_post = post_request(result, status_code=200)
    json_data = {
        "reference": "7PVGX8MEk85tgeEpVDtD",
        "email": "james@example.com",
        "amount": 20000,
        "callback_url": "http://www.google.com",
    }
    response = ravepay_api.transaction_api.initialize_transaction(**json_data)

    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]
