import re
from math import ceil
from typing import Union


def estimate_time_reading(article, words_per_minute: int = 250) -> int:
    """Estimates the reading time (in minutes) for an article's content, rounded up.
    
    Calculates based on word count and average reading speed. Uses regex to split
    the content into words for accurate counting. Returns 0 for empty content.

    Args:
        article (Article): Article instance containing the body text to analyze
        words_per_minute (int, optional): Average reading speed in WPM. 
            Defaults to 250 (average adult reading speed).
            
    Returns:
        int: Estimated reading time in minutes, rounded up. Returns 0 if article body is empty.

    Example:
        >>> article = Article(body="This is a sample article text.")
        >>> estimate_time_reading(article)
        1  # For 25 words at 250 WPM, the estimated time would be 0.1, rounded up to 1
    """
    if not article.body:
        return 0
    
    words = re.findall(r"\b\w+\b", article.body)  # More precise word matching
    total_words = len(words)
    estimated_time = total_words / words_per_minute
    return ceil(estimated_time)  # Use ceil to round up to the nearest integer
