from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from ravepay.frameworks.starlette import build_app
from ravepay.utils import RavepayAPI, get_js_script


async def post_webhook_processing(
    signature, body, ravepay_instance: RavepayAPI = None, **kwargs
):
    import pdb; pdb.set_trace()
    event, data = ravepay_instance.webhook_api.verify(
        signature, body, full_auth=True, full=True
    )


app = build_app(
    RavepayAPI, root_path="/ravepay", post_webhook_processing=post_webhook_processing
)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.route("/", methods=["GET"])
def payment_page(request: Request):
    ravepay_instance: RavepayAPI = app.state.ravepay
    redirect_url = f"/make-payment/ABCD"
    payment_info = {
        **ravepay_instance.processor_info(30),
        "currency": "ngn",
        "ref": "13ABCDJJUPP",
    }
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ravepay_instance": ravepay_instance,
            "payment_info": payment_info,
        },
    )
