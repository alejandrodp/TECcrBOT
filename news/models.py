from django.db.models import Model, TextField, IntegerField, DateTimeField, ForeignKey, DO_NOTHING, UniqueConstraint, \
    BooleanField


class Tag(Model):
    name = TextField(max_length=100)
    description = TextField(max_length=1000, null=True)
    index = IntegerField()
    category = BooleanField()


class Article(Model):
    guid = IntegerField(unique=True)
    title = TextField(max_length=500)
    pub_date = DateTimeField()
    author = TextField(max_length=100)
    link = TextField(max_length=1000)


class ArticleTagged(Model):
    article = ForeignKey(Article, DO_NOTHING)
    tag = ForeignKey(Tag, DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['article', 'tag'],
                name='articletagged_article_tag_key'
            )
        ]
