from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

@plugin_pool.register_plugin
class SimplePlugin(CMSPluginBase):
    name = _("Simple Plugin")
    render_template = "cms_simple_plugin/template.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = {}
        return context