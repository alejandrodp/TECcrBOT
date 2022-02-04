from telegram.ext import Filters
from telegram_bot_pagination import InlineKeyboardPaginator


class RegexReplyMessageFilter(Filters.regex):
    def filter(self, message):
        return super().filter(message.reply_to_message)


class InlinePaginatorCustom(InlineKeyboardPaginator):
    def add_before(self, *inline_buttons):
        for button in inline_buttons:
            self._keyboard_before.append([{
                    'text': button.text,
                    'callback_data': button.callback_data,
                }])


