# importing all the necessary modules
import speech_recognition as sr
import openai
import os
import webbrowser
import sys
import subprocess
import datetime
import requests
import json # to format the file in json format
from myAPI import my_news_api_key , my_weather_api_key, my_openAI_key # api key (news api and weather api) is imported

# this is for better understanding
openai.api_key = my_openAI_key # to avoid unnecessary problems

# saying text
def say(mytext):
    os.system(f"say {mytext}")

# taking user's audio as input and returning text as output..
def takeInput():
 r=sr.Recognizer()
 with sr.Microphone() as source:
     r.pause_threshold=1 # minimum audio energy to record
     audio=r.listen(source)
     try:
      query= r.recognize_google(audio, language='en-in') # language='bn-in' to type down the orders in bengali
      print(f"User said : {query}")
      return query
     except Exception as e:
      return "Some Error occured! Try again..."


# ai will do this
def ai(prompt):
    openai.api_key = my_openAI_key
    text=f"\nOpenAI response : {prompt}..............................\n" # empty string at first
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{prompt}",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Access the text from the first choice
    text += response['choices'][0]['text'] # adding that response to the string
    if not os.path.exists("OpenAI"):
        os.mkdir("OpenAI")
    with open (f"OpenAI/{''.join(prompt.split('intelligence')[1:]).strip()}.txt","w") as f: # will create file based on the command.
        # will split the prompt into 2, one will be til the word artificial intelligence and the rest of them will be second half.
        #.strip is used to remove the space after the word intelligence.. so that the file can organize in a well manner
        f.write(text)
        f.close()

# chatting with openAI
def chat(prompt):
    global chatStr
    chatStr += f"Bandhan:{prompt}\n Jarvis:"
    print(chatStr)
    openai.api_key = my_openAI_key
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    chatStr += f"{response['choices'][0]['text']}\n"
    say(response['choices'][0]['text'])
    return response['choices'][0]['text'] # will return the response from the ai.


# news about interest of user
def news(interest):
    api_key = my_news_api_key  # input("Your API key : ") # give your api key
    news = requests.get(
        f"https://newsapi.org/v2/everything?q={interest}&from=2024-01-1&to=2024-01-3&sortBy=popularity&sources=BBC-news&language=en&pagesize=10&apiKey={api_key}")

    news = json.loads(news.text)  # converting to a json format
    news_no = 1  # variable to keep the track the number of news
    for article in news["articles"]:  # the data inside article array is in key-value dictionary format in json file
         # will only dictate what is necesassy like : content (if user want),description and title
        print(f"News no {news_no}")
        say(f"{news_no}")
        print("Title :", article["title"]) # printing
        say(f"{article['title']}") # saying
        print("Source :", article["source"]["name"]) # printing
        print("Author :", article["author"])
        print("Description :", article["description"])
        say(f"{article['description']}")
        print("Link :", article["urlToImage"])
        print("Publish Data :", article["publishedAt"])
        print("Content : ", article["content"])
        say("Should I read content sir?") # asking user that should the assistant read content or not..
        query=takeInput()
        if "yes".lower() in query.lower():
            say("Reading content sir..")
            say(f"{article['content']}")
        elif "no".lower() in query.lower():
            pass
        else:
            say("I missed sir. Please say louder . ") # as a response of no
        print("----------------------------------------")
        news_no = news_no + 1
    # if no news is found
    if news_no == 1:
        say(f"There is no news about {interest}. Try another topic.")

# this will tell the weather of the city
def weather(city_name):
    location = city_name
    api_key = my_weather_api_key # i am using trial version for testing purposes
    weather_report = requests.get(
        f"https://api.weatherbit.io/v2.0/current?city={location}&key={api_key}&include=minutely")
    weather_report = weather_report.json()
    # print(weather_report) this will print the whole (unwanted also) info
    for info in weather_report["data"]:  # visit https://www.weatherbit.io/api/weather-current docs for more metadata
        print("city name: ", info['city_name'])
        print("temperature: ", info["app_temp"], "Degree Celcius")
        say(f"Temperature {info['app_temp']} degree Celcius")
        print("Weather:", info["weather"]["description"])
        say(f"Cloud status: {info['weather']['description']}")


# playing something on youtube
def open_page_on_youtube(queryContent, phrase): # eg: sanam+teri+kasam && sanam teri kasam
    say(f"Click to play {phrase}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={queryContent}")

# main program's code
if __name__ == "__main__":
 chatStr="" # will store the empty chat string
 say("Welcome master. I am your assistant.")
 while True:
  print("Listening...")
  query = takeInput() # user's query

  # todo: add more sites of your favorite
  sites = [ # list of all the popular searched sites
    ["Google", "https://google.com"],
    ["YouTube", "https://youtube.com"],
    ["Facebook", "https://facebook.com"],
    ["Twitter", "https://twitter.com"],
    ["Instagram", "https://instagram.com"],
    ["LinkedIn", "https://linkedin.com"],
    ["Reddit", "https://reddit.com"],
    ["Amazon", "https://amazon.com"],
    ["eBay", "https://ebay.com"],
    ["Netflix", "https://netflix.com"],
    ["Spotify", "https://spotify.com"],
    ["Pinterest", "https://pinterest.com"],
    ["Tumblr", "https://tumblr.com"],
    ["Wikipedia", "https://wikipedia.org"],
    ["GitHub", "https://github.com"],
    ["Stack Overflow", "https://stackoverflow.com"],
    ["Medium", "https://medium.com"],
    ["Quora", "https://quora.com"],
    ["BBC News", "https://bbc.com/news"],
    ["CNN", "https://cnn.com"],
  ]

  # if the user is asking to open any website
  if "open".lower() in query.lower():
   for site in sites:
      if site[0].lower() in query.lower(): # if query contains the site present in the list
       say(f"Opening {site[0]} sir.") # computer will dictate this one
       webbrowser.open(f"{site[1]}")

  # todo: add more songs paths
  elif "play music".lower() in query.lower():
      musicPATH="/home/bandhan/Downloads/song.mp3"
      # os.system(f"open {musicPATH}") is also an alternative
      opener= "open" if sys.platform == "linux" else "xdg-open"
      subprocess.call([opener,musicPATH])

  # asking for telling me time............
  elif "what's the time".lower() in query.lower():
      time = datetime.datetime.now().strftime("%H:%M:%S")
      say(f"Sir the time is {time}")

 # asking to open intellij idea IDE
  elif "idea".lower() in query.lower():
      say("Opening intellij idea sir")
      os.system("cd ~/Downloads/intellijCommunity/bin && sh idea.sh")

  # asking to generate using openAI
  elif "artificial intelligence".lower() in query.lower():
      say(f"Searching : f{query}")
      ai(query)

  # asking about the weather of a specific city
  elif "weather of".lower() in query.lower():
      parts=query.split("weather of",1)
      say("Searching weather report sir...")
      weather(parts[1])

  # to reset the chat
  elif "reset chat".lower() in query.lower():
      chatStr=""
      say("Chat has been reset")

  # assuming everytime the pattern will be like : I want to head news about + "topic"
  elif "news about".lower() in query.lower():
      parts = query.split("about", 1) # spliting the command in 2 parts
      say("Searching news for my master..")
      news(parts[1])

  # open the page of user liked content on youtube
  elif "on youtube".lower() in query.lower():
      query=query.lower() # making all the cases lower case
      split1=query.split("play",1) # play sanam teri kasam on youtube = [""]["sanam teri kasam on youtube"]
      split2=split1[1].split("on", 1) # perfect on youtube = ["sanam teri kasam"]["youtube"]
      exact_phrase=split2[0]
      myQuery=split2[0].strip().replace(" ","+") # sanam teri kasam = sanam+teri+kasam
      # Note : strip() : to remove leading and trailing whitespace ::: replace() : to replace words
      # print(myQuery)
      # print(exact_phrase)
      open_page_on_youtube(myQuery, exact_phrase) # sanam+teri+kasam , sanam teri kasam

  # stopping the assistant through breaking the loop
  elif "Stop".lower() in query.lower():
      say("Goodbye sir. Signing off")
      sys.exit()

  # if none of the type matches, it will start chating
  else:
      print("Chatting......")
      chat(query)
