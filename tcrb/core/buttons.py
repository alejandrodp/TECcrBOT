from django.core.paginator import Paginator
from telegram import InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator

from tcrb.settings import PAGINATION_LIMIT


class InlinePaginatorCustom(InlineKeyboardPaginator):
    def add_before(self, *inline_buttons):
        for button in inline_buttons:
            self._keyboard_before.append([{
                'text': button.text,
                'callback_data': button.callback_data,
            }])


class Inline:
    def __init__(self, app, sub_type, *patterns):
        self.app = app
        self.sub_type = sub_type
        self.patterns = patterns
        self.pattern_separator = ":"

    @property
    def match_pattern(self):
        return self.build_callback_pattern(True, *self.patterns)

    def build_callback_pattern(self, isHandler: bool, *data):
        data = self.pattern_separator.join(str(j)
                                           for i in (self.app, self.sub_type, data)
                                           for j in (i if isinstance(i, tuple) else (i,)))
        if isHandler:
            data = f'^{data}$'

        return data


class InlineButton(Inline):

    def __init__(self, app, sub_type, *patterns):
        super().__init__(app, sub_type, *patterns)

    def __call__(self, text, *data, **kwargs):
        return InlineKeyboardButton(
            text=text,
            callback_data=self.build_callback_pattern(False, *data),
            **kwargs)


class InlinePaginator(Inline):

    def __init__(self, app, sub_type, make_buttons, *patterns):
        super().__init__(app, sub_type, "pages", rf"(\d+)", *patterns)
        self._make_buttons = make_buttons

    def __call__(self, page_index, objects, *data, **kwargs):
        pages = Paginator(objects, PAGINATION_LIMIT)
        current_page = pages.get_page(page_index)
        buttons = self._make_buttons(current_page.object_list)

        paginator = InlinePaginatorCustom(
            page_count=pages.num_pages,
            current_page=current_page.number,
            data_pattern=self.build_callback_pattern(
                False, "pages", "{page}", *data
            )
        )

        paginator.add_before(*buttons)

        return paginator


class InlineWhooshPaginator(Inline):

    def __init__(self, app, sub_type, *patterns):
        super().__init__(app, sub_type, "pages", rf"(\d+)", *patterns)

    def __call__(self, page_index, query, *data, **kwargs):
        from tcrb.pages import build_show_page_button, index

        with index.read_index() as ix:
            pages = index.search_page(ix, query, page_index)

            buttons = (build_show_page_button(r["title"], r["ty"], r["id"]) for r in pages)

            paginator = InlinePaginatorCustom(
                page_count=pages.pagecount,
                current_page=page_index,
                data_pattern=self.build_callback_pattern(
                    False, "pages", "{page}", *data
                )
            )

            paginator.add_before(*buttons)

            return paginator
