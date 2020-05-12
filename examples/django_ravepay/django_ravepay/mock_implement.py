from ravepay.utils import RavepayAPI as MRavepayAPI

from ravepay.api import Transaction


class TestTransaction(Transaction):
    def verify_result(self, response, **kwargs):
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            return data["amount"]
        return "hello"


class RavepayAPI(MRavepayAPI):
    def verify_result(self, response, **kwargs):
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            return data["amount"]
        return "hello"
