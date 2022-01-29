from django.core.paginator import Paginator
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from news import apps
from news.models import Tag, Article

IKB = InlineKeyboardButton


def main_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text='Las noticias del TEC provienen del medio informativo '
             '<a href="https://www.tec.ac.cr/hoyeneltec">Hoy en el TEC</a>\n'
             'Seleccione una opción:',
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB('Ver últimas noticias', callback_data=f'{apps.NewsConfig.name}:category_select:58'),
                IKB('Ver por categorías', callback_data=f'{apps.NewsConfig.name}:category_list:'),
            ]
        )
    )


def categories_list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    categories = Tag.objects.filter(category=True).order_by('name')

    query.message.edit_text(
        text='Seleccione una categoría:\n\n'
             '{tags}'.format(
            tags='\n\n'.join(
                [
                    f'<b>{t.name}</b>: {t.description}'
                    for t in categories.all()
                ]
            )
        ),
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(tag.name, callback_data=f'{apps.NewsConfig.name}:category_select:{tag.id}')
                for tag in categories.all()
            ]
        )
    )


def news_list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    tag_id = query.data.split(':')[-1]

    articles = Article.objects.filter(articletagged__tag_id=tag_id).order_by('-pub_date').all()
    art_pages = Paginator(articles, 5)

    send_page(tag_id, query, 1, art_pages.num_pages, articles[:5])


def previous_page(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    data = query.data.split(':')

    current_page_index = int(data[-1])
    tag_id = data[-2]

    articles = Article.objects.filter(articletagged__tag_id=tag_id).order_by('-pub_date').all()
    art_pages = Paginator(articles, 5)

    current_page = art_pages.get_page(current_page_index)

    if current_page.has_previous():
        send_page(tag_id, query, current_page.previous_page_number(), art_pages.num_pages,
                  art_pages.get_page(current_page.previous_page_number()).object_list)
    else:
        query.answer('Esta es la primera página')


def next_page(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    data = query.data.split(':')

    current_page_index = int(data[-1])
    tag_id = data[-2]

    articles = Article.objects.filter(articletagged__tag_id=tag_id).order_by('-pub_date').all()
    art_pages = Paginator(articles, 5)

    current_page = art_pages.get_page(current_page_index)

    if current_page.has_next():
        send_page(tag_id, query, current_page.next_page_number(), art_pages.num_pages,
                  art_pages.get_page(current_page.next_page_number()).object_list)
    else:
        query.answer('No hay más páginas')


def send_page(tag_id, query, current_page, total_pages, articles):
    query.message.edit_text(
        text='Noticias de <i>{tag}</i> disponibles:\n\n{articles}'.format(
            tag=Tag.objects.get(id=tag_id).name,
            articles='\n\n'.join(
                [
                    f'{index}. {art.title}\n'
                    f'<i>Fecha de publicación: {art.pub_date.strftime("%-d/%-m/%Y %-I:%M:%S %p")}</i>'
                    for index, art in enumerate(articles, 1)
                ])
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [IKB(text=str(i), callback_data=f'{apps.NewsConfig.name}:article:{art.id}')]
                for i, art in enumerate(articles, 1)
            ] + [[
                IKB(text='Regresar a categorías️', callback_data=f'{apps.NewsConfig.name}:category_list:'),
            ]] + [[
                IKB(text='◀️', callback_data=f'{apps.NewsConfig.name}:previous_articles:{tag_id}:{current_page}'),
                IKB(text=f'{current_page}/{total_pages}', callback_data='ferwgr'),
                IKB(text='▶️', callback_data=f'{apps.NewsConfig.name}:next_articles:{tag_id}:{current_page}'),
            ]]
        )
    )


def get_article(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    data = query.data.split(':')

    article_id = int(data[-1])

    article = Article.objects.get(id=article_id)
    title = article.title
    pub_date = article.pub_date
    author = article.author
    link = article.link

    art_tags = '\n'.join([
        f'- {t.tag.name}'
        for t in article.articletagged_set.all()
    ])

    query.message.edit_text(
        text=f'<strong>Título: {title}</strong>\n'
             f'Fecha de publicación: {pub_date.strftime("%-d/%-m/%Y %-I:%M:%S %p")}\n'
             f'Autor: {author}\n'
             f'Etiquetas:\n{art_tags}\n'
             f'<a href="{link}">Enlace de la noticia</a>',
    )
