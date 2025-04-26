import pytest
from rest_framework import status
from rest_framework.test import APIClient
from articles.models import Article, Rating, Bookmark, Clap, Comment
from users.factories import UserFactory
from articles.factories import ArticleFactory, RatingFactory, BookmarkFactory, ClapFactory, CommentFactory
from django.urls import reverse
from articles.services import estimate_time_reading


@pytest.mark.django_db
class TestArticleCreateAPIView:
    def test_create_article(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        article_data = {
            'title': 'New Article',
            'body': 'This is the body of the article.',
            'image': None
        }

        response = client.post(reverse('articles:article-create'), article_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Article.objects.count() == 1
        assert Article.objects.first().title == 'New Article'

    def test_create_article_unauthenticated(self):
        client = APIClient()

        article_data = {
            'title': 'New Article',
            'body': 'This is the body of the article.',
            'image': None
        }

        response = client.post(reverse('articles:article-create'), article_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestArticleRetrieveUpdateDestroy:
    def test_get_article(self):
        user = UserFactory()
        article = ArticleFactory(author=user)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(reverse('articles:article-retrieve', kwargs={'id': article.id}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == article.title

    def test_update_article(self):
        user = UserFactory()
        article = ArticleFactory(author=user)
        client = APIClient()
        client.force_authenticate(user=user)

        updated_data = {
            'title': 'Updated Title',
            'body': 'Updated body content.',
            'image': None
        }

        response = client.put(reverse('articles:article-retrieve', kwargs={'id': article.id}), updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        article.refresh_from_db()
        assert article.title == 'Updated Title'

    def test_delete_article(self):
        user = UserFactory()
        article = ArticleFactory(author=user)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(reverse('articles:article-retrieve', kwargs={'id': article.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Article.objects.count() == 0

    def test_update_article_permission_denied(self):
        user = UserFactory()
        another_user = UserFactory()
        article = ArticleFactory(author=another_user)
        client = APIClient()
        client.force_authenticate(user=user)

        updated_data = {
            'title': 'Updated Title',
            'body': 'Updated body content.',
            'image': None
        }

        response = client.put(reverse('articles:article-retrieve', kwargs={'id': article.id}), updated_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRateArticleAPIView:
    def test_rate_article(self):
        user = UserFactory()
        article = ArticleFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        rating_data = {
            'rating': 5,
            'review': 'Excellent article!',
            'article': article.pkid
        }

        response = client.post(reverse('articles:article-rate', kwargs={'article_id': article.id}), rating_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Rating.objects.count() == 1

    def test_rate_own_article(self):
        user = UserFactory()
        article = ArticleFactory(author=user)
        client = APIClient()
        client.force_authenticate(user=user)

        rating_data = {
            'rating': "5",
            'review': 'Excellent article!',
            'article': article.pkid
        }

        response = client.post(reverse('articles:article-rate', kwargs={'article_id': article.id}), rating_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'You cannot rate your own article.' in str(response.data)


@pytest.mark.django_db
class TestBookmarkArticleAPIView:
    def test_bookmark_article(self):
        user = UserFactory()
        article = ArticleFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {"article": article.pkid}
        response = client.post(reverse('articles:article-bookmark', kwargs={'article_id': article.id}), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Bookmark.objects.count() == 1

    def test_bookmark_twice(self):
        user = UserFactory()
        article = ArticleFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'article': article.pkid}
        # First bookmark
        client.post(reverse('articles:article-bookmark', kwargs={'article_id': article.id}), data, format='json')
        # Second bookmark attempt
        response = client.post(reverse('articles:article-bookmark', kwargs={'article_id': article.id}), data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'already bookmarked' in str(response.data)


@pytest.mark.django_db
class TestClapAPIView:
    def test_clap_article(self):
        user = UserFactory()
        article = ArticleFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {"article": article.pkid}
        response = client.post(reverse('articles:article-clap', kwargs={'article_id': article.id}), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Clap.objects.count() == 1

    def test_clap_own_article(self):
        user = UserFactory()
        article = ArticleFactory(author=user)
        client = APIClient()
        client.force_authenticate(user=user)
        data = {"article": article.pkid}
        response = client.post(reverse('articles:article-clap', kwargs={'article_id': article.id}), data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'You cannot clap for your own article' in str(response.data)


@pytest.mark.django_db
class TestCommentAPIView:
    def test_comment_on_article(self):
        user = UserFactory()
        article = ArticleFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        comment_data = {
            'title': 'comment title',
            'content': 'Great article!',
            'article': article.pkid
        }

        response = client.post(reverse('articles:article-comment', kwargs={'article_id': article.id}), comment_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 1

    def test_comment_on_own_article(self):
        user = UserFactory()
        article = ArticleFactory(author=user)
        client = APIClient()
        client.force_authenticate(user=user)

        comment_data = {
            'article': article.pkid,
            'content': 'Great article!'
        }

        response = client.post(reverse('articles:article-comment', kwargs={'article_id': article.id}), comment_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'You cannot comment on your own article.' in str(response.data)


import math


@pytest.mark.django_db
def test_estimate_time_reading():
    user = UserFactory()
    article = ArticleFactory(author=user, body="This is a test article with 10 words checking time.", title="this is atitle")
    

    # Test with default words per minute (250)
    time = estimate_time_reading(article)
    assert time == 1  # 10 / 250 = 0.04, ceil = 1 (minimum is 1)

    # Test with custom words per minute
    time = estimate_time_reading(article, words_per_minute=10)
    assert time == 1  # 10 / 10 = 1.0, ceil = 1

    # Test with larger article
    article.body = "word " * 1000  # 1000 words
    article.save()
    time = estimate_time_reading(article, words_per_minute=250)
    assert time == 4  # 1000 / 250 = 4.0
