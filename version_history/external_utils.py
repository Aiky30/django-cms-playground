"""

This file contains a collection of methods that could not be included out of scope from their original libraries

"""

import functools
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_list_or_404, get_object_or_404

from cms.models import Title, CMSPlugin
from cms.plugin_pool import plugin_pool


def get_title(page, language):
    try:
        return Title.objects.get(page=page, language=language, publisher_is_draft=True)
    except Title.DoesNotExist:
        return None


# Taken from cms/models/pluginmodel -> CMSPlugin
def get_plugin(plugin_type):
    return plugin_pool.get_plugin(plugin_type)


# _get_plugin_from_id Taken from cms/admin/placeholderadmin.py
def _get_plugin_from_id(plugin_id):
    queryset = CMSPlugin.objects.values_list('plugin_type', flat=True)
    plugin_type = get_list_or_404(queryset, pk=plugin_id)[0]
    # CMSPluginBase subclass
    plugin_class = plugin_pool.get_plugin(plugin_type)
    real_queryset = plugin_class.get_render_queryset().select_related('parent', 'placeholder')
    return get_object_or_404(real_queryset, pk=plugin_id)


# dump_json Taken from djangocms_history/models
def dump_json():
    return functools.partial(json.dumps, cls=DjangoJSONEncoder)