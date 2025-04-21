import pytest
from rest_framework.exceptions import ValidationError
from articles.models import Article, Rating, Bookmark, Clap, Comment
from articles.serializers import (
    ArticleInSerializer,
    ArticleOutSerializer,
    RatingSerializer,
    BookmarkSerializer,
    ClapSerializer,
    CommentSerializer
)
from articles.factories import ArticleFactory, RatingFactory, BookmarkFactory, ClapFactory, CommentFactory
from users.factories import UserFactory


@pytest.mark.django_db
class TestArticleInSerializer:
    def test_valid_article_in_serializer(self):
        user = UserFactory()
        article_data = {
            'title': 'Test Article',
            'body': 'This is a test article body.',
            'image': None
        }
        serializer = ArticleInSerializer(data=article_data)
        assert serializer.is_valid()
        serializer.save(author=user)
        article = Article.objects.first()
        assert article.title == 'Test Article'
        assert article.body == 'This is a test article body.'

    def test_invalid_article_in_serializer_missing_field(self):
        article_data = {'body': 'Test Article body'}
        serializer = ArticleInSerializer(data=article_data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors


@pytest.mark.django_db
class TestArticleOutSerializer:
    def test_valid_article_out_serializer(self):
        user = UserFactory()
        article = ArticleFactory(author=user)
        serializer = ArticleOutSerializer(article)
        assert serializer.data['title'] == article.title
        assert serializer.data['username'] == article.author.first_name
        assert 'views_count' in serializer.data
        assert 'time_reading' in serializer.data



@pytest.mark.django_db
class TestRatingSerializer:
    def test_valid_rating_serializer(self):
        article = ArticleFactory()
        user = UserFactory()
        rating_data = {
            'rating': '5',
            'review': 'Excellent article!',
            'article': article.pkid 
        }
        serializer = RatingSerializer(data=rating_data)
        assert serializer.is_valid()
        rating = serializer.save(user=user)  # Changed from author to user
        assert rating.rating == '5'
        assert rating.review == 'Excellent article!'
        assert rating.article == article

    def test_invalid_rating_serializer(self):
        invalid_rating_data = {
            'rating': '6',  # Invalid rating (should be within 1-5)
            'review': 'Invalid rating review.',
            'article': '999'  # Non-existent article
        }
        serializer = RatingSerializer(data=invalid_rating_data)
        assert not serializer.is_valid()
      


@pytest.mark.django_db
class TestBookmarkSerializer:
    def test_valid_bookmark_serializer(self):
        user = UserFactory()
        article = ArticleFactory()
        bookmark_data = {
            'article': str(article.pkid)  # Use ID instead of title
        }
        serializer = BookmarkSerializer(data=bookmark_data)
        assert serializer.is_valid()
        bookmark = serializer.save(user=user)
        assert bookmark.article == article

    def test_invalid_bookmark_serializer(self):
        invalid_bookmark_data = {}  # Missing required article field
        serializer = BookmarkSerializer(data=invalid_bookmark_data)
        assert not serializer.is_valid()
        assert 'article' in serializer.errors


@pytest.mark.django_db
class TestClapSerializer:
    def test_valid_clap_serializer(self):
        user = UserFactory()
        article = ArticleFactory()
        clap_data = {
            'article': str(article.pkid)  # Use ID instead of title
        }
        serializer = ClapSerializer(data=clap_data)
        assert serializer.is_valid()
        clap = serializer.save(user=user)
        assert clap.article == article

    def test_invalid_clap_serializer(self):
        invalid_clap_data = {}  # Missing required article field
        serializer = ClapSerializer(data=invalid_clap_data)
        assert not serializer.is_valid()
        assert 'article' in serializer.errors


@pytest.mark.django_db
class TestCommentSerializer:
    def test_valid_comment_serializer(self):
        user = UserFactory()
        article = ArticleFactory()
        comment_data = {
            'article': str(article.pkid),  # Use ID instead of title
            'title': 'Test Comment',
            'content': 'This is a test comment content.'
        }
        serializer = CommentSerializer(data=comment_data)
        assert serializer.is_valid()
        comment = serializer.save(user=user)
        assert comment.article == article
        assert comment.title == 'Test Comment'

    def test_invalid_comment_serializer_missing_field(self):
        comment_data = {'title': 'Test Comment'}
        serializer = CommentSerializer(data=comment_data)
        assert not serializer.is_valid()
        assert 'article' in serializer.errors
        assert 'content' in serializer.errors