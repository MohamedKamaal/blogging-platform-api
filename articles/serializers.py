from rest_framework import serializers
from articles.models import Article, ArticleView, Rating, Bookmark, Clap, Comment


class ArticleInSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Articles (input).
    
    Fields:
        title (str): Article title
        body (str): Main content of the article
        image (ImageField): Banner image for the article
    """
    class Meta:
        model = Article
        fields = ["title", "body", "image"]


class ArticleOutSerializer(serializers.ModelSerializer):
    """Serializer for reading Articles (output) with extended fields.
    
    Fields:
        title (str): Article title
        body (str): Main content
        image (ImageField): Banner image
        views_count (int): Read-only count of views
        time_reading (int): Estimated reading time in minutes
        author (int): Primary key of author
        username (str): First name of the author
    """
    views_count = serializers.ReadOnlyField()
    time_reading = serializers.ReadOnlyField()
    username = serializers.CharField(source="author.first_name")

    class Meta:
        model = Article
        fields = ["title", "body", "image", "views_count", 
                 "time_reading", "author", "username"]


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for Rating model.
    
    Fields:
        rating (str): Rating value (1-5)
        review (str): Text review
        article (int): Primary key of related article
    """
    class Meta:
        model = Rating 
        fields = ["rating", "review", "article"]
        

class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for Bookmark model.
    
    Fields:
        article (int): Primary key of bookmarked article
    """
    class Meta:
        model = Bookmark 
        fields = ["article"]
        
        
class ClapSerializer(serializers.ModelSerializer):
    """Serializer for Clap model.
    
    Fields:
        article (int): Primary key of clapped article
    """
    class Meta:
        model = Clap 
        fields = ["article"]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model.
    
    Fields:
        article (int): Primary key of commented article
        title (str): Comment title/heading
        content (str): Main comment text
    """
    class Meta:
        model = Comment 
        fields = ["article", "title", "content"]