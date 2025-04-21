import re

def estimate_time_reading(article, words_per_minute=25):
    if not article.body:
        return 0.0

    words = re.findall(r"\w+", article.body)  # Regex to find words in the body
    total_words = len(words)
    estimated_time = total_words / words_per_minute
    return estimated_time
