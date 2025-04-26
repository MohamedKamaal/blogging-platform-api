import factory
from django.contrib.auth import get_user_model
from articles.models import Article, ArticleView, Rating, Bookmark, Clap, Comment
from users.factories import UserFactory
User = get_user_model()


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    author = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'Test Article {n}')
    body = factory.Faker('paragraph', nb_sentences=10)

class ArticleViewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleView

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    viewer_ip = '127.0.0.1'

class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    rating = '5'
    review = factory.Faker('sentence')

class BookmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookmark

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)

class ClapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clap

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')