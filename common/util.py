from telegram.ext import Filters


class RegexReplyMessageFilter(Filters.regex):
    def filter(self, message):
        return super().filter(message.reply_to_message)