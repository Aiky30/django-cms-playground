from django.core.serializers import serialize, deserialize

from cms.signals import post_publish

from djangocms_history.helpers import get_plugin_data

from .models import VersionHistory
from .external_utils import get_title, _get_plugin_from_id, dump_json


# A function that subscribes to the post publish signal
def _create_version(sender, **kwargs):

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

            # Using Django CMS and Django CMS history get a serializable format of the plugin
            plugin_instance = _get_plugin_from_id(plugin_id=plugin.id)
            fetched_data = get_plugin_data(plugin=plugin_instance)

            plugin_instance_list.append(fetched_data)

        cms_plugin_instance_list[placeholder.id] = plugin_instance_list
        cms_plugin_list[placeholder.id] = serialize('json', plugin_list)

    version = VersionHistory(
        page_id=page_instance.id,
        title_id=title_instance.id,
        title_data=str(serialize('json', [ title_instance ])),
        page_data=str(serialize('json', [ page_instance ])),
        placeholders=str(page_placeholders),
        plugins=str(dump_json(cms_plugin_list)),
        plugin_instance=str(dump_json(cms_plugin_instance_list)),
    )

    version.save()


post_publish.connect(_create_version)