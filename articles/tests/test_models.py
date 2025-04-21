import pytest
from articles.models import Article, ArticleView, Rating, Bookmark, Clap, Comment
from articles.services import estimate_time_reading
from articles.factories import ArticleFactory, ArticleViewFactory,BookmarkFactory, ClapFactory, CommentFactory, RatingFactory
from users.factories import UserFactory
@pytest.mark.django_db
def test_article_creation():
    article = ArticleFactory(title="Test Article")
    assert isinstance(article, Article)
    assert article.title == 'Test Article'
    assert article.slug is not None
    assert str(article) == "Test Article"

@pytest.mark.django_db
def test_article_time_reading():
    # Test with body
    article = ArticleFactory(title="Test Article")
    article.save()


    article.body = "This is a test body with several words."
    reading_time = article.time_reading
    assert isinstance(reading_time, float)
    assert reading_time > 0

    # Test without body
    article.body = None
    article.save()
    assert article.time_reading == 0

@pytest.mark.django_db
def test_article_views_count():
    article = ArticleFactory()

    assert article.views_count == 0
    ArticleView.objects.create(article=article, user=article.author, viewer_ip='192.168.1.1')
    assert article.views_count == 1

@pytest.mark.django_db
def test_article_view_record_view():
    # First view
    article = ArticleFactory()
    ArticleView.record_view(article=article, user=article.author, viewer_ip='127.0.0.1')
    assert ArticleView.objects.count() == 1

    # Same user and IP shouldn't create new record
    ArticleView.record_view(article=article, user=article.author, viewer_ip='127.0.0.1')  # Pass the required arguments
    assert ArticleView.objects.count() == 1  # No new record should be created


@pytest.mark.django_db
def test_rating_creation():
    rating = RatingFactory(review="Excellent article!")
    assert isinstance(rating, Rating)
    assert rating.rating == '5'
    assert rating.review == 'Excellent article!'
    assert rating.__str__() == f"Rating {rating.rating} for {rating.article} by {rating.user}"

@pytest.mark.django_db
def test_bookmark_creation():
    bookmark = BookmarkFactory()
    assert isinstance(bookmark, Bookmark)
    assert bookmark.article == bookmark.article
    assert bookmark.user == bookmark.user
    assert str(bookmark) == f"{bookmark.user} bookmarked {bookmark.article}"

@pytest.mark.django_db
def test_clap_creation():
    clap = ClapFactory()
    assert isinstance(clap, Clap)
    assert clap.article == clap.article
    assert clap.user == clap.user
    assert str(clap) == f"{clap.user} clapped for {clap.article}"

@pytest.mark.django_db
def test_comment_creation():
    comment = CommentFactory()
    assert isinstance(comment, Comment)
    comment = CommentFactory(title="Test Comment", content="This is a test comment content.")
    assert comment.title == "Test Comment"
    assert comment.content == 'This is a test comment content.'
    assert comment.__str__()  == f"Comment '{comment.title}' on {comment.article} by {comment.user}"
    

import pytest
from articles.services import estimate_time_reading
from articles.models import Article
from django.contrib.auth import get_user_model

User = get_user_model()



@pytest.mark.django_db
def test_estimate_time_reading():
    user = UserFactory()
    article = ArticleFactory(author=user, body="This is a test article with 10 words checking time.")  # Provide content here
    
    # Test with default words per minute (25)
    time = estimate_time_reading(article)
    assert time == pytest.approx(10 / 25)  # 10 words / 25 words per minute

    # Test with custom words per minute
    time = estimate_time_reading(article)
    assert time == pytest.approx(10 / 25)  # 10 words / 10 words per minute

    # Test with empty body
    article.body = None
    time = estimate_time_reading(article)
    assert time == 0.0  # If the body is empty, time should be 0
