

!pip install nltk
!pip install newspaper3k

#nltk
import sys
import re
import nltk
import random
from newspaper import Article

#twitter bot
import tweepy
import csv
import pandas as pd

l=input('Search Keyword ')
a='@'+l
b='#'+l   
print(a,b)

print("Some news sources retrived based on the article you searched for are shown. \n")

#input your credentials here
consumer_key = "insert_your_key"
consumer_secret = "insert_your_secret"
access_token = "insert_your_token"
access_token_secret = "insert_your_token_secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Open/Create a file to append data
csvFile = open('s.csv','a')
#Use csv Writer
csvWriter = csv.writer(csvFile)


def user(a):
  for tweet in tweepy.Cursor(api.search,q=a+'-filter:retweets',tweet_mode="extended",
                            lang="en").items(1):
      print (tweet.created_at, tweet.full_text)
      try:
          urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.full_text)
          if(tweet.entities['media'][0]["type"]=='photo'):
              media_url=tweet.entities['media'][0]["media_url"]
              print("Source:",media_url,"\n")
              print("Various other news sources which can be shown are shown below. \n")
              for i in range(len(urls)):
                summarizer(urls[i])
      except:
          pass
      csvWriter.writerow([tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

def hashtags(b):
  for tweet in tweepy.Cursor(api.search,q=b+'-filter:retweets',tweet_mode="extended",
                            lang="en").items(1):
      print (tweet.created_at, tweet.full_text)
      try:
          urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.full_text)
          if(tweet.entities['media'][0]["type"]=='photo'):
              media_url=tweet.entities['media'][0]["media_url"]
              print("Source:",media_url,"\n")
              print("Various other news sources which can be shown are shown below. \n")
              for i in range(len(urls)):
                summarizer(urls[i])
      except:
          pass
      csvWriter.writerow([tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

#article summarizer function
def summarizer(nurl):
  #Get the article
  article = Article(nurl)
  # Do some NLP
  article.download()
  article.parse()
  nltk.download('punkt')
  article.nlp()
  print(article.title)
  print(article.top_image)
  print(article.text)
  print(article.summary)

user(a)
hashtags(b)
