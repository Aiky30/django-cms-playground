from cms.signals import post_publish, post_unpublish

# https://stackoverflow.com/questions/28336299/is-there-anyway-to-hook-an-event-to-django-cms-page-publish-event
# https://docs.djangoproject.com/en/1.11/ref/signals/
# https://docs.djangoproject.com/en/1.11/topics/signals/#defining-and-sending-signals
#

post_publish.connect(self._receiver)
post_unpublish.connect(self._receiver)

def _receiver(self, sender, **kwargs):
    #logic goes here