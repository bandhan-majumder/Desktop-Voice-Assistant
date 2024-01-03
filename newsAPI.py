# it has no connection with the main.py .. This is only for newsAPI key testing
import requests
import json # to format the file in json format
from myAPI import my_news_api_key # my api key form another file is imported

interest=input("Type your interest :") # taking input from user
api_key=my_news_api_key # input("Your API key : ") # give your api key
news=requests.get(f"https://newsapi.org/v2/everything?q={interest}&from=2024-01-1&to=2024-01-3&sortBy=popularity&sources=BBC-news&language=en&pagesize=10&apiKey={api_key}")

# from=2024-01-1&to=2024-01-3 make sure to upgrade this link . For free, we can access data from past 3-4 days. else it will give error
# for details, go through the docs : https://newsapi.org/docs/endpoints/everything

news=json.loads(news.text) # converting to a json format

# print(news)

news_no=1 # variable to keep the track the number of news
for article in news["articles"]: # the data inside article array is in key-value dictionary format in json file
    print(f"News no {news_no}")
    print("Title :", article["title"])
    print("Source :", article["source"]["name"])
    print("Author :", article["author"])
    print("Description :", article["description"])
    print("Click to view the image :", article["urlToImage"])
    print("Publish Data :",article["publishedAt"])
    print("Content : ", article["content"])
    print("----------------------------------------")
    news_no=news_no+1

# if no news is available, the counter will stay same
if news_no == 1:
    print(f"There is no news about {interest}. Try another topic.")