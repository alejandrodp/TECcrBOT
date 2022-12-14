import html


class PageTy:
    def __init__(self, *, ty, model, desc, build, index=None):

        self.ty = ty
        self.desc = desc
        self.model = model
        self.index = index
        self.builder = build


def show_page(ty, page_id, reply):
    from .config import all_pages
    from .models import Page

    page_ty = all_pages.page_tys.get(ty)
    reply.expect(page_ty is not None)

    model = page_ty.model
    try:
        page = Page.objects.get(id=page_id)
        obj = model.objects.get(id=page_id)
    # model.DoesNotExist no debe ser posible
    except Page.DoesNotExist:
        reply.bad_request()

    mtime = f' (Última modificación {page.mtime})' if page.mtime else ''
    header = f'<code>#{page_id:05}</code>{mtime}\n' \
             f'<b>{html.escape(page.title)}</b> en {page_ty.desc}\n\n'

    reply.buffer_text(header)
    page_ty.builder(obj, reply)


def build_show_page_button(text, ty, page_id):
    from .buttons import show_page_button
    return show_page_button(text, ty, page_id)
