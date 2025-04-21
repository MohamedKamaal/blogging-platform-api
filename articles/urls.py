from django.urls import path 
from articles.views import (ArticleCreateAPIView, ArticleRetrieveUpdateDestroy,RateArticleAPIView,
                            BookmarkArticleAPIView, BookmarkedAPIView, ClapAPIView, CommentAPIView)

app_name="articles"

urlpatterns = [
    path("",ArticleCreateAPIView.as_view(), name="article-create"),
    path("<int:pk>/rate/",RateArticleAPIView.as_view(), name="article-rate"),
    path("<int:pk>/bookmark/",BookmarkArticleAPIView.as_view(), name="article-bookmark"),
    path("<int:pk>/comment/",CommentAPIView.as_view(), name="article-comment"),
    path("<int:pk>/clap/",ClapAPIView.as_view(), name="article-clap"),
    path("<int:pk>/bookmarked/",BookmarkedAPIView.as_view(), name="user-bookmarks"),
    path("<int:pk>/",ArticleRetrieveUpdateDestroy.as_view(), name="article-create"),
]