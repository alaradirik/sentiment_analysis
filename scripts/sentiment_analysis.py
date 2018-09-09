import pandas as pd
import numpy as np

import nltk
import re
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def clean_dataframe(data):
	# Drop unnecessery and irrelevant columns
	data = data.drop(columns=['dead', 'deleted', 'ranking', 'id', 'parent'])
	# Drop duplicates
	data = data.drop(columns=['time_ts', 'by'])
	# Convert time to datetime
	data['time'] = pd.to_datetime(data['time'], unit='s')
	return data

def extract_text(data):
	text_without_tags = list()

	# Iterate over dataframe rows
	for row in data.itertuples(index=True, name='Pandas'):
		soup = BeautifulSoup(getattr(row, "text"), features="lxml")
		article = ''
	 
		# Select and extract text from all tags
		# Remove links
		web_links = soup.find_all('a')
		for link in web_links:
			link.replace_with('')
			
		paragraphs = soup.find_all('p')
		for paragraph in paragraphs:
			article += paragraph.get_text()
		
		text_without_tags.append(article)
	return text_without_tags

def preprocess_VADER(text):
	# Remove digits with regular expression
	text = re.sub(r'\d', ' ', text)
	# Remove brackets
	text = re.sub(r'[\[]', '', text) 
	text = re.sub(r'[\]]', '', text)
	# Remove empty parantheses
	text = re.sub('()', '', text)
	# Remove less than and greater than signs
	text = re.sub(r'[<>]', '', text)
	# && is often used as a replacement of 'and'
	text = re.sub('&&', ' and ', text)
	# Remove URLs
	text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	text = re.sub(r'^http?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	# Standardize space between sentences and words separated by commas
	text = re.sub(r'(?<=[.,])(?=[^\s])', r' ', text)
	# Remove non-ASCII characters
	text = ''.join(character for character in text if ord(character)<128)
	# Replace % with percent
	text = re.sub(r'%', ' percent', text)
	# Standardize white space
	text = re.sub(r'\s+', ' ', text)
	return text

def sentiment_analysis(data):
	# Initialize sentiment analyzer model
	analyzer = SentimentIntensityAnalyzer()

	neg, neu, pos, compound = ([] for i in range(4))
	for row in data.itertuples(index=True, name='Pandas'):
		vs = analyzer.polarity_scores(getattr(row, "vader_text"))
		# Append scores to the respective lists
		neg.append(vs['neg'])
		neu.append(vs['neu'])
		pos.append(vs['pos'])
		compound.append(vs['compound'])

	# Creating sentiment score columns
	data['neg'] = neg
	data['pos'] = pos
	data['neu'] = neu
	data['compound'] = compound
	return data

def get_average_sentiment(filepath, aggregate_on):
	# Read in data into pandas dataframe
	df = pd.read_json(filepath, lines=True, orient='records', convert_dates='time')
	df = clean_dataframe(df)
	text_without_tags = extract_text(df)

	vader_text = list()
	for text in text_without_tags:
		vader_text.append(preprocess_VADER(text))

	# Drop raw text column and create a column with text preprocessed for VADER
	df['vader_text'] = vader_text
	df = df.drop(columns = ['text'])
	df = sentiment_analysis(df)

	if aggregate_on is 'year':
		df_agg = df[['time', 'neg', 'pos', 'neu', 'compound']]
		df_agg = df_agg.groupby(df['time'].dt.year).mean()
		print(df_agg)
		return df_agg
	
	elif aggregate_on is'month':
		df_agg = df[['time', 'neg', 'pos', 'neu', 'compound']]
		df_agg = df_agg.groupby(df["time"].dt.to_period("M")).mean()
		print(df_agg)
		return df_agg
	
	elif aggregate_on is'week':
		df_agg = df[['time', 'neg', 'pos', 'neu', 'compound']]
		df_agg = df_agg.groupby(df["time"].dt.to_period("W")).mean()
		print(df_agg)
		return df_agg
