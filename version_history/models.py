from django.db import models
from django.contrib.postgres.fields import JSONField

from cms.models import Page, Title
#FIXME: Can't have postgres JSON field


# TODO: Type of version (Page, Article) Should be registered in app config!!

class Version_History(models.Model):
    page = models.ForeignKey(Page, related_name='page_history')
    title = models.ForeignKey(Title, related_name='title_history')
    title_data = JSONField()
    page_data = JSONField()
    placeholders = JSONField()
    plugins = JSONField()
    plugin_instance = JSONField()
    created_date = models.DateTimeField(auto_now_add=True)