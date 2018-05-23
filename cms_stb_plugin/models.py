from cms.models.pluginmodel import CMSPlugin

from django.db import models

class STBConfiguration(CMSPlugin):
    title = models.CharField(max_length=50)