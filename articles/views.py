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
from articles.exceptions import CantClapOwnArticle,CantRateOwnArticle, CantCommentOwnArticle
# Create your views here.


class ArticleCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ArticlePagination
    queryset = Article.objects.select_related("author")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ["body"]
    ordering_fields = ["pkid"]
    
    def get_serializer_class(self):
        if self.request.method in ["GET","HEADS","OPTIONS"]:
            return ArticleOutSerializer
        
        return ArticleInSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
        

class ArticleRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Article.objects.select_related("author")
    lookup_field = 'id'
    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ArticleOutSerializer
        
        return ArticleInSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user 
        article = self.get_object()
        viewer_ip = request.META.get("REMOTE_ADDR")
        ArticleView.record_view(article,user,viewer_ip)
        return super().get(request, *args, **kwargs)
    
class RateArticleAPIView(GenericAPIView):
    serializer_class = RatingSerializer
    
    def post(self,request,article_id):
        user = request.user 
        article = get_object_or_404(Article,id=article_id)
        if article.author == user:
            raise CantRateOwnArticle
        past_rating = Rating.objects.filter(user=user,article=article).exists()
        if past_rating:
            return Response({"message":f"You already rated this article {article.title}"},status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response({"message":f"You rated this article {article.title}"},status=status.HTTP_201_CREATED)


class BookmarkArticleAPIView(GenericAPIView):
    serializer_class = BookmarkSerializer
    
    def post(self,request,article_id):
        user = request.user 
        article = get_object_or_404(Article,id=article_id)
        
        bookmarked = Bookmark.objects.filter(user=user,article=article).exists()
        if bookmarked:
            return Response({"message":f"You already bookmarked this article {article.title}"},status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response({"message":f"You bookmarked this article {article.title}"},status=status.HTTP_201_CREATED)

class BookmarkedAPIView(ListAPIView):
    serializer_class = ArticleOutSerializer
    def get_queryset(self):
        user = self.request.user 
        bookmarked_articles = Article.objects.filter(bookmarks__user=user)
        return bookmarked_articles
    
class ClapAPIView(GenericAPIView):
    serializer_class = ClapSerializer
    
    def post(self,request,article_id):
        user = request.user 
        article = get_object_or_404(Article,id=article_id)
        if article.author == user:
            raise CantClapOwnArticle
        clapped = Clap.objects.filter(user=user,article=article).exists()
        if clapped:
            return Response({"message":f"You already clapped on this article {article.title}"},status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response({"message":f"You clapped on  this article {article.title}"},status=status.HTTP_201_CREATED)


class CommentAPIView(GenericAPIView):
    serializer_class = CommentSerializer
    
    def post(self,request,article_id):
        user = request.user 
        article = get_object_or_404(Article,id=article_id)
        if article.author == user:
            raise CantCommentOwnArticle
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, article=article)
        return Response({"message":f"You commented on this article {article.title}"},status=status.HTTP_201_CREATED)


