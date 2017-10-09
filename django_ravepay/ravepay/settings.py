from django.conf import settings

RAVEPAY_SECRET_KEY = getattr(settings, "RAVEPAY_SECRET_KEY", None)
RAVEPAY_PUBLIC_KEY = getattr(settings, 'RAVEPAY_PUBLIC_KEY', None)
ALLOWED_HOSTS = getattr(settings, 'ALLOWED_HOSTS', [])
RAVEPAY_WEBHOOK_DOMAIN = getattr(settings, 'RAVEPAY_WEBHOOK_DOMAIN', None)
if RAVEPAY_WEBHOOK_DOMAIN:
    ALLOWED_HOSTS.append(RAVEPAY_WEBHOOK_DOMAIN)
RAVEPAY_FAILED_URL = getattr(
    settings, 'RAVEPAY_FAILED_URL', 'ravepay:failed_page')
RAVEPAY_SUCCESS_URL = getattr(
    settings, 'RAVEPAY_SUCCESS_URL', 'ravepay:success_page')
if settings.DEBUG:
    RAVEPAY_API_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx'
else:
    RAVEPAY_API_URL = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx'