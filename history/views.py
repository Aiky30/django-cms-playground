from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader


from cms.models import Page, Title, CMSPlugin

from django.core.serializers import serialize

from .models import FIL_History


#from django.db.models import Count, Prefetch


"""
# Create a plugin instance
UPDATE "cms_title" SET "publisher_state" = 1 WHERE ("cms_title"."page_id" = 11 AND "cms_title"."language" = 'en'); args=(1, 11, 'en')
INSERT INTO "cms_cmsplugin"
    ("path", "depth", "numchild", "placeholder_id", "parent_id", "position", "language", "plugin_type", "creation_date", "changed_date")
    VALUES ('000D', 1, 0, 12, NULL, 1, 'en', 'TextPlugin', '2018-05-17T15:33:57.483624+00:00'::timestamptz, '2018-05-17T15:33:57.492751+00:00'::timestamptz) RETURNING "cms_cmsplugin"."id";
    args=('000D', 1, 0, 12, None, 1, 'en', 'TextPlugin', datetime.datetime(2018, 5, 17, 15, 33, 57, 483624, tzinfo=<UTC>), datetime.datetime(2018, 5, 17, 15, 33, 57, 492751, tzinfo=<UTC>))


# Saving a text plugin entry
UPDATE "cms_title" SET "publisher_state" = 1 WHERE ("cms_title"."language" = 'en' AND "cms_title"."page_id" = 11); args=(1, 'en', 11)
UPDATE "cms_cmsplugin" SET "path" = '000D', "depth" = 1, "numchild" = 0, "placeholder_id" = 12, "parent_id" = NULL, "position" = 1, "language" = 'en', "plugin_type" = 'TextPlugin', "creation_date" = '2018-05-17T15:33:57.483624+00:00'::timestamptz, "changed_date" = '2018-05-17T15:35:15.777827+00:00'::timestamptz WHERE "cms_cmsplugin"."id" = 13; args=('000D', 1, 0, 12, 1, 'en', 'TextPlugin', datetime.datetime(2018, 5, 17, 15, 33, 57, 483624, tzinfo=<UTC>), datetime.datetime(2018, 5, 17, 15, 35, 15, 777827, tzinfo=<UTC>), 13)
UPDATE "djangocms_text_ckeditor_text" SET "body" = '<p>New plugin text entry!!!</p>' WHERE "djangocms_text_ckeditor_text"."cmsplugin_ptr_id" = 13; args=('<p>New plugin text entry!!!</p>', 13)
INSERT INTO "djangocms_text_ckeditor_text" ("cmsplugin_ptr_id", "body") VALUES (13, '<p>New plugin text entry!!!</p>'); args=(13, '<p>New plugin text entry!!!</p>')
UPDATE "cms_title" SET "publisher_state" = 1 WHERE ("cms_title"."language" = 'en' AND "cms_title"."page_id" = 11); args=(1, 'en', 11)
UPDATE "djangocms_text_ckeditor_text" SET "body" = '<p>New plugin text entry!!!</p>' WHERE "djangocms_text_ckeditor_text"."cmsplugin_ptr_id" = 13; args=('<p>New plugin text entry!!!</p>', 13)

"""


def _get_title(title_id):
    try:
        return Title.objects.get(id=title_id)
    except Title.DoesNotExist:
        return None


# Taken from cms/models/pluginmodel -> CMSPlugin
from cms.plugin_pool import plugin_pool


def get_plugin(plugin_type):
    return plugin_pool.get_plugin(plugin_type)

def track_instances(page_id, title_id, page_language):

    # Get the pages field list and convert it to json
    page_object = Page.objects.get(id=page_id)
    page_placeholders_list = page_object.placeholders.all()

    page_data = serialize('json', [page_object])
    page_placeholders = serialize('json', page_placeholders_list)

    page_title = _get_title(title_id)
    page_title = serialize('json', [page_title])

    # FIXME: Flawed due ot the fact that language matters here!!!
    cms_plugin_list = {}
    cms_plugin_instance_list = {}
    # Get all cms plugins for each placeholder
    for placeholder in page_placeholders_list:

        plugin_list = CMSPlugin.objects.filter(placeholder_id=placeholder, language=page_language)

        plugin_instance_list = []
        for plugin in plugin_list:
            current_plugin_instance = get_plugin(plugin.plugin_type)

            plugin_instance_list.append(current_plugin_instance)

        cms_plugin_instance_list[placeholder.id] = plugin_instance_list
        cms_plugin_list[placeholder.id] = serialize('json', plugin_list)

    page_stats = {
        'page_id': page_id,
        'linked_page_id': page_object.publisher_public_id,
    }

    return render(request, 'history/data_list.html', {
        'page_data': page_data,
        'page_title': page_title,
        'page_stats': page_stats,
        'page_placeholders': page_placeholders,
        'plugin_list': cms_plugin_list,
        'cms_plugin_instance_list': cms_plugin_instance_list,
    })

def index(request):

    page_id = request.GET['page_id']
    title_id = request.GET['title_id']
    page_language = request.GET['page_language']

    if page_id and title_id:

        #return track_instances(page_id, title_id, page_language)

        queryset_page_history = FIL_History.objects.filter(
            page_id=page_id,
            title_id=title_id,
        )
        page_history = serialize('json', queryset_page_history)

        return render(request, 'history/history_list.html', {
            'page_stats': {
                'page_id': page_id,
                'title_id': title_id,
            },
            'page_history': queryset_page_history,
            'page_history_length': len(queryset_page_history),
        })

        #return HttpResponse(template)


    return HttpResponse('Page id or title id not found')

