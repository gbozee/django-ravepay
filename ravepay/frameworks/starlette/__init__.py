import asyncio
import functools
import importlib

from ravepay.api import signals
from ravepay import utils
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.config import Config
from starlette.datastructures import URL, Secret
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

config = Config(".env")

RAVEPAY_SECRET_KEY = config("RAVEPAY_SECRET_KEY", cast=Secret)
RAVEPAY_PUBLIC_KEY = config("RAVEPAY_PUBLIC_KEY", cast=Secret)
RAVEPAY_WEBHOOK_HASH = config(
    "RAVEPAY_WEBHOOK_HASH", cast=Secret, default=utils.RavepayAPI.WEBHOOK_HASH
)


async def generate_account_number(
    request: Request, ravepay_instance: utils.RavepayAPI = None
):
    params = await request.json()
    account_name = params.get("account_name")
    client_email = params.get("client_email")
    permanent = params.get("permanent")
    order = params.get("order")
    if account_name and client_email:
        response = ravepay_instance.transaction_api.create_payment_account(
            account_name, client_email, is_permanent=permanent
        )
        if response[0]:
            return JSONResponse(
                {"status": True, "msg": response[1], "data": response[2]}
            )
        return JSONResponse({"status": False, "msg": response[1]}, status_code=400)
    return JSONResponse(
        {"status": False, "msg": "Missing account name or client email"},
        status_code=400,
    )


def verify_payment(
    request: Request, response_callback=None, ravepay_instance=None, RavepayAPI=None
):
    amount = request.query_params.get("amount")
    order = request.path_params.get("order_id")
    txrf = request.query_params.get("txref")
    code = request.query_params.get("code")
    response = ravepay_instance.verify_payment(
        txrf or code, amount=amount, amount_only=True
    )
    if response[0]:
        signals.payment_verified.send(
            sender=RavepayAPI, ref=txrf, amount=amount, order=order
        )
    return response_callback(response[0], order=order)


async def webhook_view(request: Request, background_action=None, **kwargs):
    signature = request.headers.get("verif-hash")
    body = await request.body()
    return JSONResponse(
        {"status": "Success"},
        background=BackgroundTask(background_action, signature, body, **kwargs),
    )


def build_app(
    RavepayAPI,
    root_path="",
    response_callback=None,
    post_webhook_processing=None,
    _app: Starlette = None,
    debug=False,
):
    ravepay_instance = RavepayAPI(
        public_key=str(RAVEPAY_PUBLIC_KEY),
        secret_key=str(RAVEPAY_SECRET_KEY),
        test=debug,
        django=False,
        webhook_hash=str(RAVEPAY_WEBHOOK_HASH),
    )
    if _app:
        app = _app
    else:
        app = Starlette()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def background_action(signature, body, **xkwargs):
        return ravepay_instance.webhook_api.verify(
            signature,
            body,
            full_auth=True,
            full=False,
            # loop=loop
        )

    verify_action = post_webhook_processing or background_action

    async def new_generate_account_number(request):
        return await generate_account_number(request, ravepay_instance=ravepay_instance)

    app.add_route(
        root_path + "/generate-account-no",
        new_generate_account_number,
        methods=["POST"],
    )

    async def new_webhook(request):
        return await webhook_view(
            request, background_action=verify_action, ravepay_instance=ravepay_instance
        )

    app.add_route(root_path + "/webhook", new_webhook, methods=["POST"])
    new_verify_payment = lambda request: verify_payment(
        request,
        response_callback=response_callback,
        ravepay_instance=ravepay_instance,
        RavepayAPI=RavepayAPI,
    )
    app.add_route(
        root_path + "/verify-payment/{order_id}", new_verify_payment, methods=["GET"]
    )
    app.state.ravepay = ravepay_instance
    return app
