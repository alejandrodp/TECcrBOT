from telegram.ext import CallbackQueryHandler

from bot.menu import main_menu_entry
from news import apps
from news.handlers import main_entry, categories_list, news_list, previous_page, next_page, get_article


HANDLERS = [
    main_menu_entry('Noticias TEC \U0001f4f0', main_entry),
    CallbackQueryHandler(categories_list, pattern=f'{apps.NewsConfig.name}:category_list:'),
    CallbackQueryHandler(news_list, pattern=rf'{apps.NewsConfig.name}:category_select:\d+'),
    CallbackQueryHandler(previous_page, pattern=rf'{apps.NewsConfig.name}:previous_articles:\d+:\d+'),
    CallbackQueryHandler(next_page, pattern=rf'{apps.NewsConfig.name}:next_articles:\d+:\d+'),
    CallbackQueryHandler(get_article, pattern=rf'{apps.NewsConfig.name}:article:\d+'),
]
