from django.urls import path 
from articles.views import (ArticleCreateAPIView, ArticleRetrieveUpdateDestroy,RateArticleAPIView,
                            BookmarkArticleAPIView, BookmarkedAPIView, ClapAPIView, CommentAPIView)

app_name="articles"

urlpatterns = [
    path("<uuid:article_id>/rate/",RateArticleAPIView.as_view(), name="article-rate"),
    path("<uuid:article_id>/bookmark/",BookmarkArticleAPIView.as_view(), name="article-bookmark"),
    path("<uuid:article_id>/comment/",CommentAPIView.as_view(), name="article-comment"),
    path("<uuid:article_id>/clap/",ClapAPIView.as_view(), name="article-clap"),
    path("bookmarked/",BookmarkedAPIView.as_view(), name="user-bookmarks"),
    path("<uuid:id>/",ArticleRetrieveUpdateDestroy.as_view(), name="article-retrieve"),
    path("",ArticleCreateAPIView.as_view(), name="article-create"),
]