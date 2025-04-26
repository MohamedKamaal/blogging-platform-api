import django_filters as filters
from articles.models import Article


class ArticleFilter(filters.FilterSet):
    """FilterSet for querying Article objects with flexible filtering options.

    Provides filtering capabilities for Article model with:
    - Case-insensitive partial matching on author's first name
    - Case-insensitive partial matching on article title

    Attributes:
        author (CharFilter): Filter for author's first name (contains match, case-insensitive)
        title (CharFilter): Filter for article title (contains match, case-insensitive)
    """
    
    author = filters.CharFilter(
        "author__first_name", lookup_expr="icontains"
    )
    
    title = filters.CharFilter(
        "title", "icontains"
    )
    
    class Meta:
        """Metadata options for the ArticleFilter.
        
        Specifies:
        - The model to filter (Article)
        - The fields available for filtering and their default lookup expressions
        """
        model = Article
        fields = ["author", "title"]