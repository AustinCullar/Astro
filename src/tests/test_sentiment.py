"""
Tests for the SentimentAnalysis class.
"""
import pytest

# Astro modules
from src.data_collection.sentiment import SentimentAnalysis

positive_string = 'This is amazing!'
negative_string = 'This is terrible!'
neutral_string = 'The color is blue'
nonsense_string = 'asdf gra asdg vrs sdg'
empty_string = ''


def verify_sentiment(sentiment):
    assert sentiment <= 1.0 and sentiment >= 0.0


class TestSentimentAnalysis:

    def test_add_sentiment_to_dataframe(self, logger, comment_dataframe):
        sa = SentimentAnalysis(logger)

        sa.add_sentiment_to_dataframe(comment_dataframe)

        for index, row in comment_dataframe.iterrows():
            verify_sentiment(row['PSentiment'])
            verify_sentiment(row['NSentiment'])

    @pytest.mark.parametrize('text',
                             [positive_string,
                              negative_string,
                              neutral_string,
                              nonsense_string,
                              empty_string])
    def test_get_sentiment(self, logger, text):
        sa = SentimentAnalysis(logger)

        sentiment = sa.get_sentiment(text)

        # verify that some sentiment data is returned
        verify_sentiment(sentiment[0])
        verify_sentiment(sentiment[1])
        verify_sentiment(sentiment[2])
