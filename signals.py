from django.dispatch import Signal

class Webhook_signal(Signal):
  def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
    print('[Signal Conn]::: Establishing Connection: ', receiver.__name__)
    super().connect(receiver, sender, weak, dispatch_uid)

  def send(self, sender, **named):
    print('[Signal Conn]::: Sending signal: ', sender)
    super().send(sender, **named)

  def __init__(self, providing_args=None, use_caching=False):
    print('[Signal Conn]::: Initializing')
    super().__init__()

webhook_received = Webhook_signal(providing_args=['domain', 'topic', 'data'])


