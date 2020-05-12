from ravepay.api import signals
from dispatch import receiver
import pytest


@receiver(signals.successful_payment_signal)
def signal_called(sender, **kwargs):
    kwargs.pop("signal", None)
    generic_function(**kwargs)


def generic_function(**params):
    print(params)


@receiver(signals.successful_transfer_signal)
def signal_called_2(sender, **kwargs):
    kwargs.pop("signal", None)
    generic_function(**kwargs)


@receiver(signals.failed_transfer_signal)
def signal_called_3(sender, **kwargs):
    kwargs.pop("signal", None)
    generic_function(**kwargs)


@pytest.fixture
def mock_generic_fuc(mocker):
    mock_successful_transer = mocker.patch("test_webhooks.generic_function")
    # mock_digest = mocker.patch("ravepay.api.webhook.generate_digest")
    # mock_digest.return_value = "1001"
    return mock_successful_transer


def test_successful_webhook_signals_card(mock_generic_fuc, ravepay_api):
    body = """{
    "id": 1280530,
    "txRef": "13ABCDJJUK",
    "flwRef": "FLW-MOCK-5190d67ebc44ec532a955fd0db1c795e",
    "orderRef": "URF_1589319829442_1238435",
    "paymentPlan": null,
    "paymentPage": null,
    "createdAt": "2020-05-12T21:43:49.000Z",
    "amount": 30,
    "charged_amount": 30,
    "status": "successful",
    "IP": "102.67.16.19",
    "currency": "NGN",
    "appfee": 0.84,
    "merchantfee": 0,
    "merchantbearsfee": 1,
    "customer": {
        "id": 380370,
        "phone": "234099940409",
        "fullName": "Anonymous customer",
        "customertoken": null,
        "email": "user@example.com",
        "createdAt": "2020-05-12T21:40:30.000Z",
        "updatedAt": "2020-05-12T21:40:30.000Z",
        "deletedAt": null,
        "AccountId": 24349
    },
    "payment_entity": "1555852ca0687e2e4b6e5d8dccbbb869",
    "entity": {
        "card6": "553188",
        "card_last4": "2950"
    },
    "event.type": "CARD_TRANSACTION"
}"""
    ravepay_api.webhook_api.verify(ravepay_api.webhook_hash, body)
    mock_generic_fuc.assert_called_once_with(
        data={
            "amount": 30,
            "currency": "NGN",
            "status": "successful",
            "reference": "13ABCDJJUK",
            "customer": {
                "id": 380370,
                "phone": "234099940409",
                "fullName": "Anonymous customer",
                "customertoken": None,
                "email": "user@example.com",
                "createdAt": "2020-05-12T21:40:30.000Z",
                "updatedAt": "2020-05-12T21:40:30.000Z",
                "deletedAt": None,
                "AccountId": 24349,
            },
            "entity": {"card6": "553188", "card_last4": "2950"},
        },
        payment_type="CARD_TRANSACTION",
    )


def test_successful_webhook_account_virtual_transfer(mock_generic_fuc, ravepay_api):
    body = """{
    "id": 1280545,
    "txRef": "13ABCDJJUPP",
    "flwRef": "6b04f43b136c4ec799e8029e6f31ae80",
    "orderRef": "URF_1589320781878_931435",
    "paymentPlan": null,
    "paymentPage": null,
    "createdAt": "2020-05-12T21:59:51.000Z",
    "amount": 30,
    "charged_amount": 30,
    "status": "successful",
    "IP": "102.67.16.19",
    "currency": "NGN",
    "appfee": 0.42,
    "merchantfee": 0,
    "merchantbearsfee": 1,
    "customer": {
        "id": 380370,
        "phone": "234099940409",
        "fullName": "Anonymous customer",
        "customertoken": null,
        "email": "user@example.com",
        "createdAt": "2020-05-12T21:40:30.000Z",
        "updatedAt": "2020-05-12T21:40:30.000Z",
        "deletedAt": null,
        "AccountId": 24349
    },
    "entity": {
        "id": "NO-ENTITY"
    },
    "event.type": "BANK_TRANSFER_TRANSACTION"
}"""
    ravepay_api.webhook_api.verify(ravepay_api.webhook_hash, body)
    mock_generic_fuc.assert_called_once_with(
        data={
            "amount": 30,
            "currency": "NGN",
            "status": "successful",
            "reference": "13ABCDJJUPP",
            "customer": {
                "id": 380370,
                "phone": "234099940409",
                "fullName": "Anonymous customer",
                "customertoken": None,
                "email": "user@example.com",
                "createdAt": "2020-05-12T21:40:30.000Z",
                "updatedAt": "2020-05-12T21:40:30.000Z",
                "deletedAt": None,
                "AccountId": 24349,
            },
            "entity": {"id": "NO-ENTITY"},
        },
        payment_type="BANK_TRANSFER_TRANSACTION",
    )


def test_successful_webhook_bank_account_transfer(mock_generic_fuc, ravepay_api):
    body = """{
    "id": 1280552,
    "txRef": "13ABCDJJUPP",
    "flwRef": "URF_1589321336006_3490535",
    "orderRef": "URF_1589321336006_3490535",
    "paymentPlan": null,
    "paymentPage": null,
    "createdAt": "2020-05-12T22:08:56.000Z",
    "amount": 30,
    "charged_amount": 30,
    "status": "successful",
    "IP": "102.67.16.19",
    "currency": "NGN",
    "appfee": 0.84,
    "merchantfee": 0,
    "merchantbearsfee": 1,
    "customer": {
        "id": 380370,
        "phone": "234099940409",
        "fullName": "Anonymous customer",
        "customertoken": null,
        "email": "user@example.com",
        "createdAt": "2020-05-12T21:40:30.000Z",
        "updatedAt": "2020-05-12T21:40:30.000Z",
        "deletedAt": null,
        "AccountId": 24349
    },
    "payment_entity": "0690000031",
    "entity": {
        "account_number": "0690000031",
        "first_name": "NO-NAME",
        "last_name": "NO-LNAME"
    },
    "event.type": "ACCOUNT_TRANSACTION"
}"""
    ravepay_api.webhook_api.verify(ravepay_api.webhook_hash, body)
    mock_generic_fuc.assert_called_once_with(
        data={
            "amount": 30,
            "currency": "NGN",
            "status": "successful",
            "reference": "13ABCDJJUPP",
            "customer": {
                "id": 380370,
                "phone": "234099940409",
                "fullName": "Anonymous customer",
                "customertoken": None,
                "email": "user@example.com",
                "createdAt": "2020-05-12T21:40:30.000Z",
                "updatedAt": "2020-05-12T21:40:30.000Z",
                "deletedAt": None,
                "AccountId": 24349,
            },
            "entity": {
                "account_number": "0690000031",
                "first_name": "NO-NAME",
                "last_name": "NO-LNAME",
            },
        },
        payment_type="ACCOUNT_TRANSACTION",
    )


def test_successful_transfer(mock_generic_fuc, ravepay_api):
    body = """
    {
      "event": "transfer.success",
      "data": {
        "domain": "live",
        "amount": 10000,
        "currency": "NGN",
        "source": "balance",
        "source_details": null,
        "reason": "Bless you",
        "reference": "JDJDJ",
        "recipient": {
          "domain": "live",
          "type": "nuban",
          "currency": "NGN",
          "name": "Someone",
          "details": {
            "account_number": "0123456789",
            "account_name": null,
            "bank_code": "058",
            "bank_name": "Guaranty Trust Bank"
          },
          "description": null,
          "metadata": null,
          "recipient_code": "RCP_xoosxcjojnvronx",
          "active": true
        },
        "status": "success",
        "transfer_code": "TRF_zy6w214r4aw9971",
        "transferred_at": "2017-03-25T17:51:24.000Z",
        "created_at": "2017-03-25T17:48:54.000Z"
      }
    }
    """
    ravepay_api.webhook_api.verify("1001", body)
    mock_generic_fuc.assert_called_once_with(
        transfer_code="TRF_zy6w214r4aw9971",
        data={
            "amount": 100.0,
            "recipient": {"recipient_code": "RCP_xoosxcjojnvronx"},
            "transfer_code": "TRF_zy6w214r4aw9971",
            "transferred_at": "2017-03-25T17:51:24.000Z",
            "created_at": "2017-03-25T17:48:54.000Z",
        },
    )


def test_failed_transfer(mock_generic_fuc, ravepay_api):
    body = """
    {
  "event": "transfer.failed",
  "data": {
    "domain": "test",
    "amount": 10000,
    "currency": "NGN",
    "source": "balance",
    "source_details": null,
    "reason": "Test",
    "reference": "XJKSKS",
    "recipient": {
      "domain": "live",
      "type": "nuban",
      "currency": "NGN",
      "name": "Test account",
      "details": {
        "account_number": "0000000000",
        "account_name": null,
        "bank_code": "058",
        "bank_name": "Zenith Bank"
      },
      "description": null,
      "metadata": null,
      "recipient_code": "RCP_7um8q67gj0v4n1c",
      "active": true
    },
    "status": "failed",
    "transfer_code": "TRF_3g8pc1cfmn00x6u",
    "transferred_at": null,
    "created_at": "2017-12-01T08:51:37.000Z"
  }
}
    """
    ravepay_api.webhook_api.verify("1001", body)
    mock_generic_fuc.assert_called_once_with(
        transfer_code="TRF_3g8pc1cfmn00x6u",
        data={
            "amount": 100.0,
            "recipient": {"recipient_code": "RCP_7um8q67gj0v4n1c"},
            "transfer_code": "TRF_3g8pc1cfmn00x6u",
            "transferred_at": None,
            "created_at": "2017-12-01T08:51:37.000Z",
        },
    )


def test_webhook_not_called(mock_generic_fuc, ravepay_api):
    body = """
    {
  "event": "transfer.failed",
  "data": {
    "domain": "test",
    "amount": 10000,
    "currency": "NGN",
    "source": "balance",
    "source_details": null,
    "reason": "Test",
    "reference": "XJKSKS",
    "recipient": {
      "domain": "live",
      "type": "nuban",
      "currency": "NGN",
      "name": "Test account",
      "details": {
        "account_number": "0000000000",
        "account_name": null,
        "bank_code": "058",
        "bank_name": "Zenith Bank"
      },
      "description": null,
      "metadata": null,
      "recipient_code": "RCP_7um8q67gj0v4n1c",
      "active": true
    },
    "status": "failed",
    "transfer_code": "TRF_3g8pc1cfmn00x6u",
    "transferred_at": null,
    "created_at": "2017-12-01T08:51:37.000Z"
  }
}
    """
    ravepay_api.webhook_api.verify("1101", body)
    mock_generic_fuc.assert_not_called()
