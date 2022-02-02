class PageTy:
    _tys = {}

    def __init__(self, ty, desc, index):
        existing = PageTy._tys.get(ty)
        assert existing is None, f'Page type `{desc}` collides with `{existing.desc}`'

        self.ty = ty
        self.desc = desc
        self.index = index
        PageTy._tys[ty] = self

def read_page_tys():
    import bot.settings as _ # Do not remove, preserves import order
    return PageTy._tys.items()
