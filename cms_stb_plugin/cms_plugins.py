from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import STBConfiguration

@plugin_pool.register_plugin
class STBPlugin(CMSPluginBase):
    model = STBConfiguration
    name = _("STB Plugin")
    render_template = "cms_stb_plugin/template.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(STBPlugin, self).render(context, instance, placeholder)
        return context