from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from taggit.managers import TaggableManager

from django.utils.translation import gettext as _

from common.models import TimeStampedModel
from articles.services import estimate_time_reading
User = get_user_model()
""" track article views  """
class Article(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(_("Article Title"),help_text=_("Upload article title"),
                             max_length=110)
    slug = AutoSlugField(populate_from='title', unique=True)

    image = models.ImageField(_("Article banner"),help_text=_("Upload banner for image"),
                           null=True,blank=True)
    body = models.TextField(_("Article body"),help_text=_("Article body"),
                           null=True,blank=True)
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    @property
    def time_reading(self):
        if self.body is not None:
            return estimate_time_reading(self) 
        return 0

    @property
    def views_count(self):
        return self.article_views.count()

class ArticleView(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_views")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_views")
    viewer_ip = models.GenericIPAddressField(
        _("Viewer Ip"), null=True, blank=True
    )
    class Meta:
        unique_together = ["user","article","viewer_ip"]
    
    @classmethod
    def record_view(cls, article, user, viewer_ip):
        found, instance = cls.objects.get_or_create(article=article, user=user, viewer_ip=viewer_ip)
    
    def __str__(self):
        return f"{self.article} viewed by {self.user} who has IP of {self.viewer_ip}"


class Rating(TimeStampedModel):
    class RatingChoices(models.TextChoices):
        (1,"Poor")
        (2,"Fair")
        (3,"Good")
        (4,"Very Good")
        (5,"Excellent")
        
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="ratings")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="ratings")
    rating = models.CharField(max_length=1,choices=RatingChoices.choices)
    review = models.CharField(max_length=200)
    
    class Meta:
        unique_together= ["user","article"]
        

class Bookmark(TimeStampedModel):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="bookmarks")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookmarks")
    class Meta:
        unique_together= ["user","article"]

class Clap(TimeStampedModel):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="claps")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="claps")
    class Meta:
        unique_together= ["user","article"]
    



class Comment(TimeStampedModel):
   article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="comments")

   title = models.CharField(max_length=110)
   content = models.TextField()