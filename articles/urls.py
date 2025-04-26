from django.urls import path
from articles.views import (
    ArticleCreateAPIView,
    ArticleRetrieveUpdateDestroy,
    RateArticleAPIView,
    BookmarkArticleAPIView,
    BookmarkedAPIView,
    ClapAPIView,
    CommentAPIView
)

app_name = "articles"

urlpatterns = [
    # Article rating endpoints
    path(
        "<uuid:article_id>/rate/",
        RateArticleAPIView.as_view(),
        name="article-rate"
    ),
    
    # Article bookmark endpoints
    path(
        "<uuid:article_id>/bookmark/",
        BookmarkArticleAPIView.as_view(),
        name="article-bookmark"
    ),
    path(
        "bookmarked/",
        BookmarkedAPIView.as_view(),
        name="user-bookmarks"
    ),
    
    # Article interaction endpoints
    path(
        "<uuid:article_id>/comment/",
        CommentAPIView.as_view(),
        name="article-comment"
    ),
    path(
        "<uuid:article_id>/clap/",
        ClapAPIView.as_view(),
        name="article-clap"
    ),
    
    # Core article CRUD endpoints
    path(
        "<uuid:id>/",
        ArticleRetrieveUpdateDestroy.as_view(),
        name="article-retrieve"
    ),
    path(
        "",
        ArticleCreateAPIView.as_view(),
        name="article-create"
    ),
]