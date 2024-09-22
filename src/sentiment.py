"""
Functionality for determining the sentiment of a given comment/string. This
approach utilizes the Natural Language Toolkit in combination with
SentiWordNet.

This logic was informed by the following article written by "AI & Tech by Nidhika, PhD":
https://medium.com/@nidhikayadav/sentiment-analysis-with-python-sentiwordnet-fd07ffc557
"""
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

class SentimentAnalysis:
	def __init__(self, logger):
		self.logger = logger.get_logger()

	def get_sentiment(self, comment: str) -> ():
		token_comment = nltk.word_tokenize(comment)
		pos_tag_comment = nltk.pos_tag(token_comment)

		positive_sentiment = 0.0
		negative_sentiment = 0.0

		for word_tag in pos_tag_comment:
			word = word_tag[0]
			tag = word_tag[1]

			if tag.startswith('J'):
				tag = wn.ADJ
			elif tag.startswith('R'):
				tag = wn.ADV
			elif tag.startswith('N'):
				tag = wn.NOUN
			else:
				continue

			# Get synonyms for current word, 'synset'.
			word_synset = wn.synsets(word, pos=tag)
			if not word_synset:
				continue

			# Naive/inexpensive approach: use the first word in the set
			chosen_synset = word_synset[0]

			# Retrieve sentiment score for the given synonym from SentiWordNet
			senti_word_net = swn.senti_synset(chosen_synset.name())

			positive_sentiment += senti_word_net.pos_score()
			negative_sentiment += senti_word_net.neg_score()
			objectivity = 1 - (positive_sentiment + negative_sentiment)

			return (positive_sentiment, negative_sentiment, objectivity)

	def get_sentiment_multiple(self, comments: list) -> list:
		comments_with_sentiment = []

		for comment in comments:
			# comment_sentiment: (user, comment, timestamp)
			comment_sentiment = self.get_sentiment(comment[1])

			comment_with_sentiment = comment + comment_sentiment

			comments_with_sentiment.append(comment_with_sentiment)

		return comments_with_sentiment
			
