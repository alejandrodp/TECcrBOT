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
                IKB('Ver últimas noticias', callback_data=f'{apps.NewsConfig.name}:last_news:'),
            ]
        )
    )


def last_news(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.message.edit_text(
        text='Seleccione una categoría:',
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(tag.name, callback_data=f'{apps.NewsConfig.name}:category_news:{tag.id}')
                for tag in Tag.objects.filter(category=True).all()
            ]
        )
    )


def category_list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    tag_id = query.data.split(':')[-1]

    articles = Article.objects.filter(articletagged__tag_id=tag_id).order_by('pub_date').all()
    art_pages = Paginator(articles, 5)

    query.message.edit_text(
        text='Seleccione una noticia:',
        reply_markup=InlineKeyboardMarkup(
            [
                [IKB(text=art.title, callback_data=f'{apps.NewsConfig.name}:article:{art.id}')]
                for art in articles[:5]
            ] + [[
                IKB(text='', callback_data=f'{apps.NewsConfig.name}:previous_article:0'),
                IKB(text='', callback_data=f'{apps.NewsConfig.name}:previous_article:0'),
            ]]
        )
    )







