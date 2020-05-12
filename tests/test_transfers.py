import pytest
from ravepay.utils import RavepayAPI
from ravepay import utils


def test_create_recipient_success(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "BENEFICIARY-CREATED",
        "data": {
            "id": 6845,
            "account_number": "0690000031",
            "bank_code": "044",
            "fullname": "Forrest Green",
            "date_created": "2020-05-08T20:57:11.000Z",
            "bank_name": "ACCESS BANK NIGERIA",
        },
    }
    bank_list = {
        "status": "success",
        "message": "SUCCESS",
        "data": {
            "Banks": [
                {
                    "Id": 191,
                    "Code": "044",
                    "Name": "Access Bank",
                    "IsMobileVerified": None,
                    "branches": None,
                }
            ]
        },
    }
    mock_get = get_request(bank_list, status_code=200)
    mock_post = post_request(result, status_code=200)
    response = ravepay_api.transfer_api.create_recipient(
        "Forrest Green", "0690000031", "Access Bank", country="ng"
    )
    mock_assertion(
        mock_get, "/v2/banks/NG", params={"public_key": ravepay_api.public_key}
    )
    mock_assertion(
        mock_post,
        "/v2/gpx/transfers/beneficiaries/create",
        json={
            "account_bank": "044",
            "account_number": "0690000031",
            "seckey": ravepay_api.secret_key,
        },
    )
    mock_assertion(
        mock_post,
        "/v2/gpx/transfers/beneficiaries/create",
        json={
            "account_bank": "044",
            "account_number": "0690000031",
            "seckey": ravepay_api.secret_key,
        },
    )
    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]


def test_create_recipient_fail(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    pass


def test_initial_transfer_success(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "TRANSFER-CREATED",
        "data": {
            "id": 122887,
            "account_number": "0690000031",
            "bank_code": "044",
            "fullname": "Forrest Green",
            "date_created": "2020-05-08T21:32:28.000Z",
            "currency": "NGN",
            "amount": 50,
            "fee": 10.75,
            "status": "NEW",
            "reference": "a1f12d9ff3569915",
            "meta": None,
            "narration": "Payment of x services",
            "complete_message": "",
            "requires_approval": 0,
            "is_approved": 1,
            "bank_name": "ACCESS BANK NIGERIA",
        },
    }
    bank_list = {
        "status": "success",
        "message": "QUERIED-BENEFICIARIES",
        "data": {
            "page_info": {"total": 1, "current_page": 1, "total_pages": 1},
            "payout_beneficiaries": [
                {
                    "id": 6845,
                    "account_number": "0690000031",
                    "bank_code": "044",
                    "fullname": "Forrest Green",
                    "meta": None,
                    "date_created": "2020-05-08T20:57:11.000Z",
                    "bank_name": "ACCESS BANK NIGERIA",
                }
            ],
        },
    }
    mock_get = get_request(bank_list, status_code=200)
    mock_post = post_request(result, status_code=200)
    response = ravepay_api.transfer_api.initialize_transfer(50, 6854)
    mock_assertion(
        mock_post,
        "/v2/gpx/transfers/create",
        json={
            "recipient": 6845,
            "amount": 50,
            "narration": "",
            "currency": "NGN",
            "beneficiary_name": "Forrest Green",
            "seckey": ravepay_api.secret_key,
        },
    )
    mock_assertion(
        mock_get,
        "/v2/gpx/transfers/beneficiaries",
        params={"seckey": ravepay_api.secret_key},
    )
    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]


def test_initial_transfer_failed(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    pass


def test_get_transfer_success(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    pass


def test_get_transfer_failed(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    pass


def test_transfer_bulk_success(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "BULK-TRANSFER-CREATED",
        "data": {
            "id": 2783,
            "date_created": "2020-05-08T22:05:26.000Z",
            "approver": "N/A",
        },
    }
    bulk_result = {
        "status": "success",
        "message": "QUERIED-TRANSFERS",
        "data": {
            "page_info": {"total": 1, "current_page": 1, "total_pages": 1},
            "transfers": [
                {
                    "id": 122901,
                    "account_number": "0690000032",
                    "bank_code": "044",
                    "fullname": "Pastor Bright",
                    "date_created": "2020-05-09T06:23:22.000Z",
                    "currency": "NGN",
                    "debit_currency": None,
                    "amount": 11.5,
                    "fee": 10.75,
                    "status": "SUCCESSFUL",
                    "reference": "09ea9d5f2cde9200_PMCKDU_5",
                    "meta": None,
                    "narration": "Bulk transfer 1",
                    "approver": None,
                    "complete_message": "Successful",
                    "requires_approval": 0,
                    "is_approved": 1,
                    "bank_name": "ACCESS BANK NIGERIA",
                }
            ],
        },
    }
    mock_get = get_request(bulk_result, status_code=200)
    mock_post = post_request(result, status_code=200)
    response = ravepay_api.transfer_api.bulk_transfer(
        [
            {
                "amount": 200,
                "account_no": "0000323232",
                "currency": "ngn",
                "bank_code": "044",
            }
        ],
        reason="March Salary",
    )
    mock_assertion(
        mock_post,
        "/v2/gpx/transfers/create_bulk",
        json={
            "bulk_data": [
                {
                    "Bank": "044",
                    "Account Number": "0000323232",
                    "Amount": 200,
                    "Currency": "NGN",
                    "Narration": "March Salary",
                }
            ],
            "title": "March Salary",
            "seckey": ravepay_api.secret_key,
        },
    )
    mock_assertion(
        mock_get,
        "/v2/gpx/transfers",
        params={"seckey": ravepay_api.secret_key, "batch_id": 2783},
    )
    assert response[0]
    assert response[1] == "Bulk successful"
    assert response[2] == bulk_result["data"]["transfers"][0]


def test_transfer_bulk_failed(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "BULK-TRANSFER-CREATED",
        "data": {
            "id": 2783,
            "date_created": "2020-05-08T22:05:26.000Z",
            "approver": "N/A",
        },
    }
    bulk_result = {
        "status": "success",
        "message": "QUERIED-TRANSFERS",
        "data": {
            "page_info": {"total": 0, "current_page": 0, "total_pages": 0},
            "transfers": [],
        },
    }
    mock_get = get_request(bulk_result, status_code=200)
    mock_post = post_request(result, status_code=200)
    response = ravepay_api.transfer_api.bulk_transfer(
        [
            {
                "amount": 200,
                "account_no": "0000323232",
                "currency": "ngn",
                "bank_code": "044",
            }
        ],
        reason="March Salary",
    )
    mock_assertion(
        mock_post,
        "/v2/gpx/transfers/create_bulk",
        json={
            "bulk_data": [
                {
                    "Bank": "044",
                    "Account Number": "0000323232",
                    "Amount": 200,
                    "Currency": "NGN",
                    "Narration": "March Salary",
                }
            ],
            "title": "March Salary",
            "seckey": ravepay_api.secret_key,
        },
    )
    mock_assertion(
        mock_get,
        "/v2/gpx/transfers",
        params={"seckey": ravepay_api.secret_key, "batch_id": 2783},
    )
    assert not response[0]
    assert response[1] == "Failed Bulk Transfer"


def test_get_balance(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "WALLET-BALANCE",
        "data": {
            "Id": 22160,
            "ShortName": "NGN",
            "WalletNumber": "3163000169946",
            "AvailableBalance": 0,
        },
    }
    mock_post = post_request(result, status_code=200)
    response = ravepay_api.transfer_api.check_balance()
    mock_assertion(
        mock_post,
        "/v2/gpx/balance",
        json={"currency": "NGN", "seckey": ravepay_api.secret_key},
    )
    assert response == {"currency": "NGN", "balance": 0}


def test_get_banks(
    mock_assertion, post_request, get_request, ravepay_api: utils.RavepayAPI
):
    result = {
        "status": "success",
        "message": "SUCCESS",
        "data": {
            "Banks": [
                {
                    "Id": 132,
                    "Code": "560",
                    "Name": "Page MFBank",
                    "IsMobileVerified": None,
                    "branches": None,
                },
                {
                    "Id": 133,
                    "Code": "304",
                    "Name": "Stanbic Mobile Money",
                    "IsMobileVerified": None,
                    "branches": None,
                },
            ],
            "Token": {
                "access_token": None,
                "refresh_token": None,
                "token_type": None,
                "expires_in": 0,
            },
            "Status": "Success",
            "Message": "successul",
            "Data": None,
            "AllTransactions": None,
        },
    }
    mock_get = get_request(result, status_code=200)
    response = ravepay_api.transfer_api.get_banks(country="gh")
    mock_assertion(
        mock_get, "/v2/banks/GH", params={"public_key": ravepay_api.public_key}
    )
    assert response[0]
    assert response[1] == result["message"]
    assert response[2] == result["data"]

