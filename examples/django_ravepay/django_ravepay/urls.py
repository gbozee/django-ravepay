"""django_ravepay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.contrib import admin
from django.views.generic import TemplateView
from dispatch import receiver
from ravepay.api import signals


version = django.get_version().split(".")
if int(version[0]) >= 2:
    from django.urls import re_path as url, include
else:
    from django.conf.urls import url
    from django.conf.urls import url, include


@receiver(signals.successful_payment_signal)
def on_successful_payment(sender, **kwargs):
    import pdb

    pdb.set_trace()
    pass


if int(version[0]) > 1:
    ravepay_route = url(
        "^ravepay/",
        include(("ravepay.frameworks.django.urls", "ravepay"), namespace="ravepay"),
    )
else:
    ravepay_route = (
        url(
            r"^ravepay/", include("ravepay.frameworks.django.urls", namespace="ravepay")
        ),
    )


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="sample.html"), name="home"),
    url(r"^admin/", admin.site.urls),
    ravepay_route,
]
