from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from django.utils.translation import gettext as _

from common.models import TimeStampedModel
from articles.services import estimate_time_reading

User = get_user_model()


class Article(TimeStampedModel):
    """
    Represents a blog article or post in the system.
    
    Inherits from TimeStampedModel for automatic creation/update timestamps.
    Tracks author, content, metadata, and engagement metrics.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(_("Article Title"), help_text=_("Upload article title"),
                           max_length=110)
    slug = AutoSlugField(populate_from='title', unique=True)
    image = models.ImageField(_("Article banner"), help_text=_("Upload banner for image"),
                           null=True, blank=True)
    body = models.TextField(_("Article body"), help_text=_("Article body"))
    tags = TaggableManager()
    
    def __str__(self):
        """Returns string representation of the article (its title)."""
        return str(self.title)
    
    @property
    def time_reading(self):
        """Calculates estimated reading time for the article in minutes.
        
        Returns:
            int: Estimated reading time in minutes, 0 if body is empty
        """
        if self.body is not None:
            return estimate_time_reading(self) 
        return 0

    @property
    def views_count(self):
        """Returns total number of views for this article.
        
        Returns:
            int: Count of all ArticleView instances for this article
        """
        return self.article_views.count()


class ArticleView(TimeStampedModel):
    """
    Tracks individual views of articles, including anonymous views by IP.
    
    Records who viewed which article and from which IP address.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_views")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_views")
    viewer_ip = models.GenericIPAddressField(
        _("Viewer Ip"), null=True, blank=True
    )
    
    class Meta:
        """Ensures each unique viewer (user or IP) is only counted once per article."""
        unique_together = ["user", "article", "viewer_ip"]
    
    @classmethod
    def record_view(cls, article, user, viewer_ip):
        """Records a view event for an article.
        
        Args:
            article (Article): The article being viewed
            user (User): The user viewing (None for anonymous)
            viewer_ip (str): IP address of the viewer
        """
        found, instance = cls.objects.get_or_create(article=article, user=user, viewer_ip=viewer_ip)
    
    def __str__(self):
        """Returns formatted string of the viewing event."""
        return f"{self.article} viewed by {self.user} who has IP of {self.viewer_ip}"


class Rating(TimeStampedModel):
    """
    Represents a user's rating and review of an article.
    
    Allows users to rate articles on a 5-point scale with optional text review.
    """
    class RatingChoices(models.TextChoices):
        """Available rating choices with descriptive labels."""
        POOR = '1', _("Poor")
        FAIR = '2', _("Fair")
        GOOD = '3', _("Good")
        VERY_GOOD = '4', _("Very Good")
        EXCELLENT = '5', _("Excellent")
        
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    rating = models.CharField(max_length=1, choices=RatingChoices.choices)
    review = models.CharField(max_length=200)
    
    class Meta:
        """Ensures each user can only rate an article once."""
        unique_together = ["user", "article"]
    
    def __str__(self):
        """Returns formatted string of the rating."""
        return f"Rating {self.rating} for {self.article} by {self.user}"


class Bookmark(TimeStampedModel):
    """
    Represents a user saving an article for later reference.
    
    Simple many-to-many relationship between users and articles.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    
    class Meta:
        """Prevents duplicate bookmarks by the same user for the same article."""
        unique_together = ["user", "article"]
    
    def __str__(self):
        """Returns formatted string of the bookmark."""
        return f"{self.user} bookmarked {self.article.title}"


class Clap(TimeStampedModel):
    """
    Represents a user's appreciation for an article (similar to a 'like').
    
    Simple many-to-many relationship tracking who 'clapped' for which articles.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="claps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="claps")
    
    class Meta:
        """Prevents duplicate claps by the same user for the same article."""
        unique_together = ["user", "article"]
    
    def __str__(self):
        """Returns formatted string of the clap action."""
        return f"{self.user} clapped for {self.article.title}"


class Comment(TimeStampedModel):
    """
    Represents a user's comment on an article.
    
    Contains both a title and content body for structured feedback.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=110)
    content = models.TextField()
    
    def __str__(self):
        """Returns formatted string of the comment."""
        return f"Comment '{self.title}' on {self.article} by {self.user}"