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
list=["Manhattan, NY","Brooklyn, NY","Bronx, NY","Queens, NY","Staten Island, NY","Westchester, NY","Nassau, NY","Suffolk, NY","Atlantic County, NJ","Bergen County, NJ","Burlington County, NJ","Camden County, NJ","Cape May County, NJ","Cumberland County, NJ","Essex County, NJ","Gloucester County, NJ","Hudson County, NJ","Hunterdon County, NJ","Mercer County, NJ","Middlesex County, NJ","Monmouth County, NJ","Morris County, NJ","Ocean County, NJ","Passaic County, NJ","Salem County, NJ","Somerset County, NJ","Sussex County, NJ","Union County, NJ","Warren County, NJ"]
print("Some news sources retrieved based on the article you searched for are shown. \n")


#input your credentials here
consumer_key = "3XlvwneYeiizWuJx2GxfJM0tn"
consumer_secret = "8QhxM6xYIHobqZTA9JLlBRbFFZoQIInQlG5JjbSMA5onF4auPm"
access_token = "2200824096-Lnn8IM0rGgKUw0BaTAk01ITnOp3gv3an5iwgHcM"
access_token_secret = "g0Dk9NDbtGuvyh2HqYudAauGm5ghWs9bZ62osYqkjv3O4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# Open/Create a file to append data
csvFile = open('corona.csv','a')
#Use csv Writer
csvWriter = csv.writer(csvFile)


def user(a):
  for tweet in tweepy.Cursor(api.search,q=a+'-filter:retweets',tweet_mode="extended",lang="en").items(100):     
      flag = 0
      for i in range(len(list)):
        # print(tweet.user.location)
        if list[i] == tweet.user.location:
          print(tweet.user.location)                           
          print (tweet.created_at, tweet.full_text)
          try:
              urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.full_text)
              if(tweet.entities['media'][0]["type"]=='photo'):
                  media_url=tweet.entities['media'][0]["media_url"]
                  print("Source:",media_url,"\n")
                  print("Various other news sources which can be shown are below. \n")
                  for i in range(len(urls)):
                    summarizer(urls[i])
          except:
              pass
          csvWriter.writerow([tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

def hashtags(b):
  for tweet in tweepy.Cursor(api.search,q=b+'-filter:retweets',tweet_mode="extended",lang="en").items(100):
      flag = 0
      for i in range(len(list)):
        # print(tweet.user.location)
        if list[i] == tweet.user.location:
          print(tweet.user.location)
          flag = 1                           
          print (tweet.created_at, tweet.full_text)
          try:
              urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.full_text)
              if(tweet.entities['media'][0]["type"]=='photo'):
                  media_url=tweet.entities['media'][0]["media_url"]
                  print("Source:",media_url,"\n")
                  print("Various other news sources which can be shown are below. \n")
                  for i in range(len(urls)):
                    summarizer(urls[i])
          except:
              pass
          csvWriter.writerow([tweet.created_at,tweet.user.location,tweet.user.location, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

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

hashtags(b)
user(a)



  
