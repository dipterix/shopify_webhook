from .signals import webhook_received
import hashlib,base64,hmac
from django.http import HttpResponse
from .models import Shopify
import json

from django.contrib.auth import get_user_model

def webhook_validate(func):
  '''
  Decorator to view functions, usually sent from shopify webhook engine
  '''
  def f(*args, **kwargs):
    request = args[0]
    shop_url = request.META.get('HTTP_X_SHOPIFY_SHOP_DOMAIN','')
    name = shop_url.split('.')[0]
    user_model = get_user_model()
    shop = Shopify.objects.get(**{
            "user__%s" % user_model.USERNAME_FIELD: name
        })
    is_passed = shop.webhook_validate(request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256'), request.body)
    if is_passed:
      kwargs['_topic'] = request.META.get('HTTP_X_SHOPIFY_TOPIC')
      kwargs['_data'] = json.loads(request.body.decode(encoding='utf-8'))
      kwargs['_domain'] = name
      kwargs['_shop'] = shop
      return func(*args, **kwargs)
    else:
      return HttpResponse(status = 403)
  return f