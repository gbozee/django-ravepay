from django.conf.urls import url
from . import settings, views

urlpatterns = [
    url(r'^verify-payment/(?P<order>[\w.@+-]+)/$',
        views.verify_payment, name='verify_payment'),
    url(r'^failed-verification/(?P<order_id>[\w.@+-]+)/$',
        views.FailedView.as_view(), name='failed_verification'),
    url(r'^successful-verification/(?P<order_id>[\w.@+-]+)/$',
        views.SuccessView.as_view(),
        name='successful_verification'),
    url(r'^failed-page/$',
        views.TemplateView.as_view(template_name='ravepay/failed-page.html'), name='failed_page'),
    url(r'^success-page/$',
        views.TemplateView.as_view(template_name='ravepay/success-page.html'), name='success_page'),
]
