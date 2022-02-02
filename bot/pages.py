class PageTy:
    _tys = {}

    def __init__(self, ty, desc, index, page_builder):
        existing = PageTy._tys.get(ty)
        assert existing is None, f'Page type `{desc}` collides with `{existing.desc}`'

        self.ty = ty
        self.desc = desc
        self.index = index
        self.page_builder = page_builder
        PageTy._tys[ty] = self

def read_page_tys():
    #########################################
    # Do not remove, preserves import order #
    #########################################
    import bot.settings as _ 

    return PageTy._tys
