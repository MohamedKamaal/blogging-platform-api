import re
def estimate_time_reading(article, words_per_minute=25):
    words = re.findall(
        pattern=r"\w+",
        string = article.body
    )
    total_words = len(words)
    estimated_time = total_words / words_per_minute
    return estimated_time