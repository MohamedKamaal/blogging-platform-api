import factory
from django.contrib.auth import get_user_model
from articles.models import Article, ArticleView, Rating, Bookmark, Clap, Comment
from users.factories import UserFactory

User = get_user_model()


class ArticleFactory(factory.django.DjangoModelFactory):
    """Factory for creating Article test instances.
    
    Generates articles with:
    - Sequentially numbered titles ('Test Article 1', 'Test Article 2', etc.)
    - Random paragraph content (10 sentences)
    - Associated author from UserFactory
    """
    class Meta:
        model = Article

    author = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'Test Article {n}')
    body = factory.Faker('paragraph', nb_sentences=10)



class ArticleViewFactory(factory.django.DjangoModelFactory):
    """Factory for creating ArticleView test instances.
    
    Generates view records with:
    - Associated article from ArticleFactory
    - Associated user from UserFactory
    - Default IP address '127.0.0.1'
    """
    class Meta:
        model = ArticleView

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    viewer_ip = '127.0.0.1'


class RatingFactory(factory.django.DjangoModelFactory):
    """Factory for creating Rating test instances.
    
    Generates ratings with:
    - Associated article from ArticleFactory
    - Associated user from UserFactory
    - Default rating of '5' (Excellent)
    - Random review sentence
    """
    class Meta:
        model = Rating

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    rating = '5'
    review = factory.Faker('sentence')


class BookmarkFactory(factory.django.DjangoModelFactory):
    """Factory for creating Bookmark test instances.
    
    Generates bookmarks with:
    - Associated article from ArticleFactory
    - Associated user from UserFactory
    """
    class Meta:
        model = Bookmark

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)


class ClapFactory(factory.django.DjangoModelFactory):
    """Factory for creating Clap test instances.
    
    Generates claps with:
    - Associated article from ArticleFactory
    - Associated user from UserFactory
    """
    class Meta:
        model = Clap

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for creating Comment test instances.
    
    Generates comments with:
    - Associated article from ArticleFactory
    - Associated user from UserFactory
    - Random sentence as title
    - Random paragraph as content
    """
    class Meta:
        model = Comment

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')