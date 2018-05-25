import functools
import json

from django.core.serializers import serialize, deserialize
from django.core.serializers.json import DjangoJSONEncoder

from cms.plugin_pool import plugin_pool
from cms.signals import post_publish
from cms.models import Page, Title, CMSPlugin

from djangocms_history.helpers import get_plugin_data

from .models import VersionHistory


"""

Questions:
    The plugin architecture is very confusing to follow
    Is it best to use the plugin pool and serialize that way or track the DB tables down and duplicate them.
    No way to serialize the plugin instance models, is there a cleaner way to achieve this without using magic?
    When will the plugin pool docs be populated? http://docs.django-cms.org/en/latest/reference/plugins.html

"""


# Taken from cms/models/pluginmodel -> CMSPlugin
def get_plugin(plugin_type):
    return plugin_pool.get_plugin(plugin_type)


def get_title(page, language):
    try:
        return Title.objects.get(page=page, language=language, publisher_is_draft=True)
    except Title.DoesNotExist:
        return None


# Taken from cms/admin/placeholderadmin.py
from django.shortcuts import get_list_or_404, get_object_or_404, render

def _get_plugin_from_id(plugin_id):
    queryset = CMSPlugin.objects.values_list('plugin_type', flat=True)
    plugin_type = get_list_or_404(queryset, pk=plugin_id)[0]
    # CMSPluginBase subclass
    plugin_class = plugin_pool.get_plugin(plugin_type)
    real_queryset = plugin_class.get_render_queryset().select_related('parent', 'placeholder')
    return get_object_or_404(real_queryset, pk=plugin_id)


# Taken from djangocms_history/models
dump_json = functools.partial(json.dumps, cls=DjangoJSONEncoder)


def _publish_receiver(sender, **kwargs):

    page_instance = kwargs['instance']
    page_language = kwargs['language']

    title_instance = get_title(page_instance, page_language)

    page_placeholders_list = page_instance.placeholders.all()
    page_placeholders = serialize('json', page_placeholders_list)

    # FIXME: Flawed due to the fact that language matters here!!!
    cms_plugin_list = {}
    cms_plugin_instance_list = {}
    # Get all cms plugins for each placeholder
    for placeholder in page_placeholders_list:

        plugin_list = placeholder.cmsplugin_set.all()
        #plugin_list = CMSPlugin.objects.filter(placeholder_id=placeholder, language=page_language)

        plugin_instance_list = []
        for plugin in plugin_list:

            plugin_instance = _get_plugin_from_id(plugin_id=plugin.id)

            fetched_data = get_plugin_data(plugin=plugin_instance)

            plugin_instance_list.append(dump_json(fetched_data))

        cms_plugin_instance_list[placeholder.id] = plugin_instance_list
        cms_plugin_list[placeholder.id] = serialize('json', plugin_list)

    version = VersionHistory(
        page_id=page_instance.id,
        title_id=title_instance.id,
        title_data= serialize('json', [ title_instance ]),
        page_data= serialize('json', [ page_instance ]),
        placeholders= page_placeholders,
        plugins= cms_plugin_list,
        plugin_instance = cms_plugin_instance_list,
    )

    version.save()


post_publish.connect(_publish_receiver)
#post_unpublish.connect(_receiver)