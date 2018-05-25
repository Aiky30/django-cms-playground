from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize, deserialize

from .models import VersionHistory


def create_version(request):

    page_id = request.GET['page_id']
    title_id = request.GET['title_id']
    page_language = request.GET['page_language']

    if page_id and title_id:

        #return track_instances(page_id, title_id, page_language)

        queryset_page_history = VersionHistory.objects.filter(
            page_id=page_id,
            title_id=title_id,
        ).order_by(
            '-created_date'
        )

        #return HttpResponse(template)
        return render(request, 'version_history/history_list.html', {
            'revert_url': '/version_history/rewind/',
            'page_stats': {
                'page_id': page_id,
                'title_id': title_id,
            },
            'page_history': queryset_page_history,
            'page_history_length': len(queryset_page_history),
        })

    return HttpResponse('Page id or title id not found')


def rewind(request):

    try:
        chosen_instance = VersionHistory.objects.get(id=request.POST['history'])

        title_data = chosen_instance.title_data
        page_data = chosen_instance.page_data
        placeholders = chosen_instance.placeholders
        plugins = chosen_instance.plugins
        plugin_instance = chosen_instance.plugin_instance
        created_date = chosen_instance.created_date


        # Get the draft page id, title id and update the data on the draft using the serialized data


        # Restore the title
        title_data = deserialize("json", title_data)
        title = title_data[0]
        title_id = title.object.id
        del(title.object.id)
        new_title = title.save()

        page_data = deserialize("json", page_data)


    except VersionHistory.DoesNotExist as err:
        return HttpResponse('Version cannot be found')



