from cms.signals import post_publish

from cms.models import Page, Title, CMSPlugin

from django.core.serializers import serialize


from .models import FIL_History
# https://stackoverflow.com/questions/28336299/is-there-anyway-to-hook-an-event-to-django-cms-page-publish-event
# https://docs.djangoproject.com/en/1.11/ref/signals/
# https://docs.djangoproject.com/en/1.11/topics/signals/#defining-and-sending-signals
#

# Taken from cms/models/pluginmodel -> CMSPlugin
from cms.plugin_pool import plugin_pool


def get_plugin(plugin_type):
    return plugin_pool.get_plugin(plugin_type)


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

    page_placeholders_list = page_instance.placeholders.all()
    page_placeholders = serialize('json', page_placeholders_list)

    # FIXME: Flawed due ot the fact that language matters here!!!
    cms_plugin_list = {}
    #cms_plugin_instance_list = {}
    # Get all cms plugins for each placeholder
    for placeholder in page_placeholders_list:

        plugin_list = CMSPlugin.objects.filter(placeholder_id=placeholder, language=page_language)

        plugin_instance_list = []
        for plugin in plugin_list:
            current_plugin_instance = get_plugin(plugin.plugin_type)

            plugin_instance_list.append(current_plugin_instance)

        #cms_plugin_instance_list[placeholder.id] = plugin_instance_list
        cms_plugin_list[placeholder.id] = serialize('json', plugin_list)

    version = FIL_History(
        page=page_instance,
        title=title_instance,
        title_data= serialize('json', [ title_instance ]),
        page_data= serialize('json', [ page_instance ]),
        placeholders= page_placeholders,
        plugins= cms_plugin_list,
    )

    version.save()


post_publish.connect(_publish_receiver)
#post_unpublish.connect(_receiver)