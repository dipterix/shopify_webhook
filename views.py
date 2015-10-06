from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .validators import webhook_validate
import json
from .models import *

@csrf_exempt
@webhook_validate
def product_creation(request, **kwargs):
  #   data = json.loads(request.body.decode(encoding='utf-8'))
  #   topic = request.META.get('HTTP_X_SHOPIFY_TOPIC')
  shop = kwargs['_shop']
  shop.send_signal(kwargs['_topic'], kwargs['_data'])
#   shop.send_signal(topic = 'products/create', data = json.loads(data))
  return HttpResponse(status=200)