from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from cms.models import Page, Title, CMSPlugin

from .models import Version_History

#from django.db.models import Count, Prefetch

from django.core.serializers import serialize, deserialize

def _get_title(title_id):
    try:
        return Title.objects.get(id=title_id)
    except Title.DoesNotExist:
        return None

# Taken from cms/models/pluginmodel -> CMSPlugin
from cms.plugin_pool import plugin_pool

def get_plugin(plugin_type):
    return plugin_pool.get_plugin(plugin_type)


def rewind(request):

    try:
        chosen_instance = Version_History.objects.get(id=request.POST['history'])

        title_data = chosen_instance.title_data
        page_data = chosen_instance.page_data
        placeholders = chosen_instance.placeholders
        plugins = chosen_instance.plugins
        plugin_instance = chosen_instance.plugin_instance
        created_date = chosen_instance.created_date

        title_data = deserialize("json", title_data)
        page_data = deserialize("json", page_data)


    except Version_History.DoesNotExist as err:
        return HttpResponse('Version cannot be found')


def index(request):

    page_id = request.GET['page_id']
    title_id = request.GET['title_id']
    page_language = request.GET['page_language']

    if page_id and title_id:

        #return track_instances(page_id, title_id, page_language)

        queryset_page_history = Version_History.objects.filter(
            page_id=page_id,
            title_id=title_id,
        ).order_by(
            '-created_date'
        )

        return render(request, 'version_history/history_list.html', {
            'revert_url': '/version_history/rewind/',
            'page_stats': {
                'page_id': page_id,
                'title_id': title_id,
            },
            'page_history': queryset_page_history,
            'page_history_length': len(queryset_page_history),
        })

        #return HttpResponse(template)


    return HttpResponse('Page id or title id not found')

