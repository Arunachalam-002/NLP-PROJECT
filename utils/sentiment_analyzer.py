from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")

def analyze_sentiment(texts):
    sid = SentimentIntensityAnalyzer()
    combined = " ".join(texts)
    return sid.polarity_scores(combined)
