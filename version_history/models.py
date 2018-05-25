from django.db import models
#from django.contrib.postgres.fields import JSONField

#FIXME: Can't use postgres JSON field for compatibility, woudl be good to use it if it's available i.e. a check if exists
# TODO: Type of version (Page, Article) Should be registered in app config!!


class VersionHistory(models.Model):
    page_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    title_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    title_data = models.TextField(blank=True)
    page_data = models.TextField(blank=True)
    placeholders = models.TextField(blank=True)
    plugins = models.TextField(blank=True)
    plugin_instance = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)