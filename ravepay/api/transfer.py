from .base import BaseClass
from dateutil import parser


class RavepayException(Exception):
    pass


class Transfer(BaseClass):
    path = "/v2/gpx"

    def get_banks(self, country="ng"):
        path = "/v2/banks/{}".format(country.upper())
        response = self.make_request(
            "GET", path, params={"public_key": self.public_key}
        )
        result = self.result_format(response)
        return result

    def get_bank(self, bank_name, country="ng"):
        _, _, data, _ = self.get_banks(country=country)
        banks = data["Banks"]
        item = [x for x in banks if bank_name.lower() in x["Name"].lower()]
        if item:
            return item[0]

    def get_bank_code(self, *args, **kwargs):
        result = self.get_bank(*args, **kwargs)
        if result:
            return result[0]["Code"]

    def create_recipient(
        self, account_name, account_id, bank, country="ng", verify=True
    ):
        path = self.build_path("/transfers/beneficiaries/create")
        json = {
            "seckey": self.secret_key,
            "account_number": account_id,
            "account_bank": self.get_bank_code(bank),
        }
        response = self.make_request("POST", path, json=json)
        result = self.result_format(response)
        if result[0]:
            if verify:
                assert result[2]["fullname"].lower() == account_name.lower()
        return result

    def initialize_transfer(self, amount, recipient, reason="", currency="ngn"):
        path = self.build_path("/transfers/create")
        recipient_info = self.get_recipient_info(recipient)
        if not recipient_info:
            raise RavepayException("Invalid Recipient Passed")
        json = {
            "seckey": self.secret_key,
            "narration": reason,
            "amount": amount,
            "recipient": recipient,
            "beneficiary_name": recipient_info["fullname"],
            "currency": currency.upper(),
        }
        req = self.make_request("POST", path, json=json)
        return self.result_format(req)

    def get_all_recipients(self):
        path = self.build_path("/transfers/beneficiaries")
        req = self.make_request("GET", path, params={"seckey": self.secret_key})
        return self.result_format(req)

    def get_recipient_info(self, recipient_id):
        result = self.get_all_recipients()
        if result:
            all_values = result[2]["payout_beneficiaries"]
            value = [x for x in all_values if x["id"] == recipient_id]
            if value:
                return value[0]

    def check_balance(self, currency="ngn"):
        path = self.build_path("/balance")
        result = self.make_request(
            "POST", path, json={"currency": currency.upper(), "seckey": self.secret_key}
        )

        data = result.json()
        if data["status"] != "success":
            raise RavepayException("Invalid Key sent.")
        return [
            {"currency": x["ShortName"], "balance": x["AvailableBalance"]}
            for x in data.get("data")
        ]

    def get_transfer(self, transfer_id):
        """Fetch the transfer for a given recipient"""
        result = self.get_all_transfers()
        if result:
            transfers = result[2]["transfers"]
            found = [x for x in transfers if x["id"] == transfer_id]
            if found:
                return found[0]

    def get_all_transfers(self):
        path = self.build_path("/transfers")
        req = self.make_request("GET", path, params={"seckey": self.secret_key})
        return self.result_format(req)

    def bulk_transfer(self, array_of_recipient_with_amount, reason="",country="ng"):
        transform = [
            {"Amount": x["amount"], "Recipient": x["recipient"],'currency','Narration':reason,}
            for x in array_of_recipient_with_amount
        ]
        path = self.build_path("/transfers/create_bulk")
        json_data = {"currency": "NGN", "source": "balance", "transfers": transform}
        req = self.make_request("POST", path, json=json_data)
        return self.result_format(req, lambda x: (x["status"], x["message"]))
