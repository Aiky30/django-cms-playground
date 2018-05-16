from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar_base import CMSToolbar

from cms.constants import RIGHT, REFRESH_PAGE, LEFT

@toolbar_pool.register
class MyToolbar(CMSToolbar):

    def populate(self):

        url = 'toolbar/index'
        name = 'History'


        """
        self.toolbar.add_button(
            name,
            url,
            active=False,
            disabled=False,
            extra_classes=None,
            extra_wrapper_classes=None,
            side=RIGHT,
            position=None)
        """


        history_menu = self.toolbar.get_or_create_menu(
            'history',
            name,
            side=LEFT,
            position=None)

        history_menu.add_modal_item(
            'Show history',
            url,
            active=False,
            disabled=False,
            extra_classes=None,
            on_close=REFRESH_PAGE,
            side=LEFT,
            position=None
        )

        """
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('History'))
        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
        menu = admin_menu.get_or_create_menu('poll-menu', _('Polls'), position=position)
        menu.add_sideframe_item('Poll overview', url=url)
        admin_menu.add_break('poll-break', position=menu)
        """

"""
from django.core.urlresolvers import reverse
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar


@toolbar_pool.register
class MyToolbarToolbar(CMSToolbar):

    def populate(self):
        if self.is_current_app:
            menu = self.toolbar.get_or_create_menu('poll-app', 'Polls')
            url = reverse('admin:polls_poll_changelist')
            menu.add_sideframe_item(_('Poll overview'), url=url)
"""