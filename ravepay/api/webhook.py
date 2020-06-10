import json

from ravepay.api import signals


def charge_data(raw_data, full_auth=False, full=False):
    if full:
        return raw_data
    return {
        "amount": raw_data["amount"],
        "currency": raw_data["currency"],
        "status": raw_data["status"],
        "reference": raw_data["txRef"],
        "customer": raw_data["customer"],
        "entity": raw_data.get("entity"),
    }


class Webhook:
    def __init__(self, secret_key, webhook_hash):
        self.secret_key = secret_key
        self.webhook_has = webhook_hash

    def verify(
        self,
        unique_code,
        request_body,
        use_default=False,
        full_auth=False,
        full=False,
        **kwargs
    ):
        if unique_code == self.webhook_has:
            payload = json.loads(request_body)
            if payload.get("event.type") in [
                "CARD_TRANSACTION",
                "BANK_TRANSFER_TRANSACTION",
                "ACCOUNT_TRANSACTION",
            ]:
                kwargs["data"] = charge_data(payload, full_auth=full_auth, full=full)
                kwargs["payment_type"] = payload.get("event.type")
            if use_default:
                signal_func = signals.event_signal
            else:
                options = {
                    "CARD_TRANSACTION": signals.successful_payment_signal,
                    "BANK_TRANSFER_TRANSACTION": signals.successful_payment_signal,
                    "ACCOUNT_TRANSACTION": signals.successful_payment_signal,
                }
                try:
                    signal_func = options[payload["event.type"]]
                except KeyError:
                    signal_func = signals.event_signal
            signal_func.send(sender=self, **kwargs)
            try:
                event = payload['event.type']
            except KeyError:
                event = None
            return event, kwargs
