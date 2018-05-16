from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader


from cms.models import Page, Title, Placeholder

from django.core.serializers import serialize


import json

def index(request):

    page_id = request.GET['page_id']

    if page_id is not None:

        # Get the pages field list and convert it to json
        page_object = Page.objects.get(id=page_id)

        page_placeholders = Placeholder.objects.filter()

        data = serialize('json', [ page_object])

        page_stats = {
            'page_id': page_id,
            'linked_page_id': page_object.publisher_public_id,
        }

        return render(request, 'history/history_list.html', {
            'data': data,
            'page_stats': page_stats,
        })

        #return HttpResponse(template)


    return HttpResponse('Page id not found')

