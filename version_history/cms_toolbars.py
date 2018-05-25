from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.constants import RIGHT, REFRESH_PAGE, LEFT
from cms.api import get_page_draft, can_change_page

from .external_utils import get_title

# Contains code and methods Taken from PageToolbar in CMS cms_toobar.py

@toolbar_pool.register
class VersionHistoryToolbar(CMSToolbar):

    def init_from_request(self):
        self.page = get_page_draft(self.request.current_page)
        self.title = get_title(self.page, self.current_lang)

    def populate(self):

        self.init_from_request()

        current_page = self.request.current_page

        if self.title and current_page:

            current_page_id = current_page.id

            url = '/version_history/view_versions/?page_id=%s&title_id=%s&page_language=%s' % (current_page_id, self.title.id, self.current_lang)
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
                position=None
            )

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