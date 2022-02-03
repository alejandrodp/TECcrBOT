from bot.menu import main_menu_entry
from news.handlers import main_entry, categories_list, news_list, previous_page, next_page, get_article, handlers


main_menu_entry('Noticias TEC \U0001f4f0', main_entry)
handlers.add_callback_query_handler(categories_list, 'category_list')
handlers.add_callback_query_handler(news_list, 'category_select', r'\d+')
handlers.add_callback_query_handler(previous_page, 'previous_articles', r'\d+', r'\d+')
handlers.add_callback_query_handler(next_page, 'next_articles', r'\d+', r'\d+')
handlers.add_callback_query_handler(get_article, 'article', r'\d+')
