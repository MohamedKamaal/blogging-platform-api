import django_filters as filters
from articles.models import Article

class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(
        "author__first_name",lookup_expr="icontains"
    )
    
    title = filters.CharFilter(
        "title","icontains"
    )
    
    class Meta:
        model = Article 
        fields = ["author","title"]