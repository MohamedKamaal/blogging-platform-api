from django.shortcuts import get_object_or_404
from articles.serializers import ArticleInSerializer, ArticleOutSerializer, RatingSerializer, BookmarkSerializer, ClapSerializer, CommentSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from articles.models import Article, ArticleView, Rating, Bookmark, Clap, Comment
from rest_framework.response import Response
from rest_framework import status
from articles.paginations import ArticlePagination
from articles.permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from articles.filters import ArticleFilter
from articles.exceptions import CantClapOwnArticle, CantRateOwnArticle, CantCommentOwnArticle


class ArticleCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows:
    - Listing all articles (GET)
    - Creating new articles (POST)
    
    Features:
    - Pagination support
    - Filtering, searching and ordering
    - Different serializers for input/output
    - Automatic author assignment on creation
    """
    permission_classes = [IsAuthenticated]
    pagination_class = ArticlePagination
    queryset = Article.objects.select_related("author")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ["body"]
    ordering_fields = ["pkid"]
    
    def get_serializer_class(self):
        """Returns appropriate serializer based on request method"""
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return ArticleOutSerializer
        return ArticleInSerializer

    def perform_create(self, serializer):
        """Automatically sets the author to the current user"""
        author = self.request.user
        serializer.save(author=author)


class ArticleRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows:
    - Retrieving single article (GET)
    - Updating article (PUT/PATCH)
    - Deleting article (DELETE)
    
    Features:
    - Author permission checks
    - Article view tracking
    - Different serializers for read/write operations
    """
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Article.objects.select_related("author")

    def get_serializer_class(self):
        """Returns appropriate serializer based on request method"""
        if self.request.method == "GET":
            return ArticleOutSerializer
        return ArticleInSerializer

    def get(self, request, *args, **kwargs):
        """Records article view before returning response"""
        user = request.user 
        article = self.get_object()
        viewer_ip = request.META.get("REMOTE_ADDR")
        ArticleView.record_view(article, user, viewer_ip)
        return super().get(request, *args, **kwargs)


class RateArticleAPIView(GenericAPIView):
    """
    API endpoint for rating articles
    
    POST /articles/<uuid:article_id>/rate/
    - Allows authenticated users to rate articles
    - Prevents authors from rating their own articles
    - Prevents duplicate ratings
    """
    serializer_class = RatingSerializer
    
    def post(self, request, article_id):
        """Handles article rating submission"""
        user = request.user 
        article = get_object_or_404(Article, id=article_id)
        
        if article.author == user:
            raise CantRateOwnArticle
            
        if Rating.objects.filter(user=user, article=article).exists():
            return Response(
                {"message": f"You already rated this article {article.title}"},
                status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response(
            {"message": f"You rated this article {article.title}"},
            status=status.HTTP_201_CREATED
        )


class BookmarkArticleAPIView(GenericAPIView):
    """
    API endpoint for bookmarking articles
    
    POST /articles/<uuid:article_id>/bookmark/
    - Allows authenticated users to bookmark articles
    - Prevents duplicate bookmarks
    """
    serializer_class = BookmarkSerializer
    
    def post(self, request, article_id):
        """Handles article bookmark submission"""
        user = request.user 
        article = get_object_or_404(Article, id=article_id)
        
        if Bookmark.objects.filter(user=user, article=article).exists():
            return Response(
                {"message": f"You already bookmarked this article {article.title}"},
                status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response(
            {"message": f"You bookmarked this article {article.title}"},
            status=status.HTTP_201_CREATED
        )


class BookmarkedAPIView(ListAPIView):
    """
    API endpoint for listing user's bookmarked articles
    
    GET /articles/bookmarked/
    - Returns paginated list of articles bookmarked by current user
    """
    serializer_class = ArticleOutSerializer
    
    def get_queryset(self):
        """Returns queryset of articles bookmarked by current user"""
        user = self.request.user 
        return user.bookmarks.all()


class ClapAPIView(GenericAPIView):
    """
    API endpoint for clapping on articles
    
    POST /articles/<uuid:article_id>/clap/
    - Allows authenticated users to clap for articles
    - Prevents authors from clapping their own articles
    - Prevents duplicate claps
    """
    serializer_class = ClapSerializer
    
    def post(self, request, article_id):
        """Handles article clap submission"""
        user = request.user 
        article = get_object_or_404(Article, id=article_id)
        
        if article.author == user:
            raise CantClapOwnArticle
            
        if Clap.objects.filter(user=user, article=article).exists():
            return Response(
                {"message": f"You already clapped on this article {article.title}"},
                status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response(
            {"message": f"You clapped on this article {article.title}"},
            status=status.HTTP_201_CREATED
        )


class CommentAPIView(GenericAPIView):
    """
    API endpoint for commenting on articles
    
    POST /articles/<uuid:article_id>/comment/
    - Allows authenticated users to comment on articles
    - Prevents authors from commenting on their own articles
    """
    serializer_class = CommentSerializer
    
    def post(self, request, article_id):
        """Handles article comment submission"""
        user = request.user 
        article = get_object_or_404(Article, id=article_id)
        
        if article.author == user:
            raise CantCommentOwnArticle
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response(
            {"message": f"You commented on this article {article.title}"},
            status=status.HTTP_201_CREATED
        )