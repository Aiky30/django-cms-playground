from cms.signals import post_publish

from cms.models import Page, Title, CMSPlugin

from django.core.serializers import serialize, deserialize

from .models import Version_History


"""

Create the STB plugin!!!

Questions:
    The plugin architecture is very confusing to follow
    Is it best to use the plugin pool and serialize that way or track the DB tables down and duplicate them.
    No way to serialize the plugin instance models
    - When will the plugin pool docs be populated: http://docs.django-cms.org/en/latest/reference/plugins.html

"""


# Taken from cms/models/pluginmodel -> CMSPlugin
from cms.plugin_pool import plugin_pool


def get_plugin(plugin_type):
    return plugin_pool.get_plugin(plugin_type)


def get_title(page, language):
    try:
        return Title.objects.get(page=page, language=language, publisher_is_draft=True)
    except Title.DoesNotExist:
        return None

from django.utils.encoding import force_text
from djangocms_history.utils import get_plugin_model


from djangocms_history.utils import get_plugin_fields
# Taken from nad modified djangocms_history.helpers import get_plugin_data
def get_plugin_data(plugin, only_meta=False):
    if only_meta:
        custom_data = None
    else:
        plugin_fields = get_plugin_fields(plugin.plugin_type)

        # Edited
        _plugin_data = serialize('python', (plugin,), fields=plugin_fields)[0]
        #_plugin_data = serialize('json', (plugin,), fields=plugin_fields)


        custom_data = _plugin_data['fields']

    plugin_data = {
        'pk': plugin.pk,
        'creation_date': plugin.creation_date,
        'position': plugin.position,
        'plugin_type': plugin.plugin_type,
        'parent_id': plugin.parent_id,
        'data': custom_data,
    }
    return plugin_data

def _publish_receiver(sender, **kwargs):
    #logic goes here

    page_instance = kwargs['instance']
    page_language = kwargs['language']

    title_instance = get_title(page_instance, page_language)

    page_placeholders_list = page_instance.placeholders.all()
    page_placeholders = serialize('json', page_placeholders_list)

    # FIXME: Flawed due ot the fact that language matters here!!!
    cms_plugin_list = {}
    cms_plugin_instance_list = {}
    # Get all cms plugins for each placeholder
    for placeholder in page_placeholders_list:

        plugin_list = CMSPlugin.objects.filter(placeholder_id=placeholder, language=page_language)

        plugin_instance_list = []
        for plugin in plugin_list:

            current_plugin_instance = get_plugin(plugin.plugin_type)

            fetched_data = get_plugin_data(plugin=plugin)

            current_plugin_model = get_plugin_model(plugin.plugin_type)
            data_model = force_text(current_plugin_model._meta)

            data = {
                'model': data_model,
                'fields': fetched_data['data'],
            }

            deserialized = list(deserialize('python', [data]))[0]


            #deserialized_plugin = list(serialize('json', [current_plugin_model]))


            plugin_instance_list.append(data)

        cms_plugin_instance_list[placeholder.id] = plugin_instance_list

        cms_plugin_list[placeholder.id] = serialize('json', plugin_list)

    version = Version_History(
        page=page_instance,
        title=title_instance,
        title_data= serialize('json', [ title_instance ]),
        page_data= serialize('json', [ page_instance ]),
        placeholders= page_placeholders,
        plugins= cms_plugin_list,
        plugin_instance = cms_plugin_instance_list,
    )

    version.save()


post_publish.connect(_publish_receiver)
#post_unpublish.connect(_receiver)