from django.db import models
from django.conf import settings
import hashlib,base64,hmac
from .signals import webhook_received

class Shopify(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  webhook_key = models.CharField(max_length = 254, null = False, blank = True, default = '')
  api_key = models.CharField(max_length = 254, null = False, blank = True, default = '')
  api_secret = models.CharField(max_length = 254, null = False, blank = True, default = '')

  @property
  def name(self):
    return getattr(self.user, self.user.USERNAME_FIELD)

  @property
  def url(self):
    return "%s.myshopify.com" % self.name

  def webhook_validate(self, digest, body):
    '''
    digest: request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256')
    body: request.body
    '''
    hm = hmac.new(self.webhook_key.encode(encoding='utf-8'),
                  body,hashlib.sha256)
    hm_digest_verify = base64.b64encode(hm.digest()).decode(encoding='utf-8')
    if hm_digest_verify == digest:
      return True
    return False

  def send_signal(self, topic, data):
    webhook_received.send(sender = self.__class__, domain = self.name, topic = topic, data = data)