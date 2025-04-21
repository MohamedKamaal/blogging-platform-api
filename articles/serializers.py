from rest_framework import serializers
from articles.models import Article, ArticleView, Rating, Bookmark, Clap, Comment


class ArticleInSerializer(serializers.ModelSerializer):
    """ add tags """
    class Meta:
        model = Article
        fields = ["title","body","image"]

class ArticleOutSerializer(serializers.ModelSerializer):
    views_count = serializers.ReadOnlyField()
    time_reading = serializers.ReadOnlyField()
    username = serializers.CharField(source="author.first_name")
    class Meta:
        model = Article
        fields = ["title","body","image","views_count","time_reading","author","username"]




class RatingSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="article.title")
    class Meta:
        model = Rating 
        fields = ["rating","review","title"]
        
    

class BookmarkSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="article.title")
    class Meta:
        model = Bookmark 
        fields = ["rating","review","title"]
        
        
class ClapSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="article.title")
    class Meta:
        model = Clap 
        fields = ["title"]

class CommentSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="article.title")
    class Meta:
        model = Rating 
        fields = ["article","title","body"]