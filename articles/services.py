import re
from typing import Union
from articles.models import Article


def estimate_time_reading(article: Article, words_per_minute: int = 250) -> float:
    """Estimates the reading time (in minutes) for an article's content.
    
    Calculates based on word count and average reading speed. Uses regex to split
    the content into words for accurate counting. Returns 0 for empty content.

    Args:
        article (Article): Article instance containing the body text to analyze
        words_per_minute (int, optional): Average reading speed in WPM. 
            Defaults to 250 (average adult reading speed).
            
    Returns:
        float: Estimated reading time in minutes, rounded to 1 decimal place.
            Returns 0.0 if article body is empty.

    Example:
        >>> article = Article(body="This is a sample article text.")
        >>> estimate_time_reading(article)
        0.1  # For 25 words at 250 WPM
    """
    if not article.body:
        return 0.0

    words = re.findall(r"\w+", article.body)  # Regex to find words in the body
    total_words = len(words)
    estimated_time = total_words / words_per_minute
    return round(estimated_time, 1)