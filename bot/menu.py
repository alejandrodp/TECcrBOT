from telegram.ext import MessageHandler, Filters

_main_menu = []

def read_main_menu():
    import bot.settings as _
    return _main_menu

def main_menu_entry(title, handler):
    if not _main_menu or len(_main_menu[-1]) >= 2:
        _main_menu.append([])

    _main_menu[-1].append(title)
    return MessageHandler(Filters.text(title), handler)
