from django.conf.urls import url
from django.http import JsonResponse
from django.shortcuts import reverse, render, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView, RedirectView
from . import settings
from .models import RavePay
from .utils import RavepayAPI


def verify_payment(request, order):
    instance = get_object_or_404(RavePay, txref=order)
    code = request.GET.get('code')
    ravepay_instance = RavepayAPI()
    response = ravepay_instance.verify_payment(code, instance.amount)
    if response:
        instance.date_paid = timezone.now()
        instance.save()
        return JsonResponse({'url': reverse('ravepay:successful_verification', args=[instance.txref])})
    return JsonResponse({"url": reverse('ravepay:failed_verification', args=[instance.txref])})


class FailedView(RedirectView):
    permanent = True
    pattern_name = settings.RAVEPAY_FAILED_URL


class SuccessView(RedirectView):
    permanent = True
    pattern_name = settings.RAVEPAY_SUCCESS_URL


urlpatterns = [
    url(r'^failed-verification/(?P<order_id>[\w.@+-]+)/$',
        FailedView.as_view(), name='failed_verification'),
    url(r'^successful-verification/(?P<order_id>[\w.@+-]+)/$',
        SuccessView.as_view(),
        name='successful_verification'),
    url(r'^failed-page/$',
        TemplateView(template_name='ravepay/failed-page.html'), name='failed_page'),
    url(r'^success-page/$',
        TemplateView(template_name='ravepay/succes-page.html'), name='success_page'),

]
