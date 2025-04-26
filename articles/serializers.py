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
    
    class Meta:
        model = Rating 
        fields = ["rating","review","article"]
        
    

class BookmarkSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Bookmark 
        fields = ["article"]
        
        
class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap 
        fields = ["article"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = ["article","title","content"]
