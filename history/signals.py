from cms.signals import post_publish

from cms.models import Title

from .models import FIL_History
# https://stackoverflow.com/questions/28336299/is-there-anyway-to-hook-an-event-to-django-cms-page-publish-event
# https://docs.djangoproject.com/en/1.11/ref/signals/
# https://docs.djangoproject.com/en/1.11/topics/signals/#defining-and-sending-signals
#


def get_title(page, language):
    try:
        return Title.objects.get(page=page, language=language, publisher_is_draft=True)
    except Title.DoesNotExist:
        return None

def _publish_receiver(sender, **kwargs):
    #logic goes here

    page_instance = kwargs['instance']
    page_language = kwargs['language']

    title_instance = get_title(page_instance, page_language)

    version = FIL_History(
        page=page_instance,
        title=title_instance,
        title_data= {},
        page_data= {},
        placeholders= {},
        plugins= {}
    )

    version.save()


post_publish.connect(_publish_receiver)
#post_unpublish.connect(_receiver)