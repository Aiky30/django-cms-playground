from django.db import models
from django.contrib.postgres.fields import JSONField

#FIXME: Can't use postgres JSON field for compatibility
# TODO: Type of version (Page, Article) Should be registered in app config!!


class VersionHistory(models.Model):
    page_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    title_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    title_data = JSONField()
    page_data = JSONField()
    placeholders = JSONField()
    plugins = JSONField()
    plugin_instance = JSONField()
    created_date = models.DateTimeField(auto_now_add=True)