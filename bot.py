from twython import Twython, TwythonError
import time
import random
import json

credentials = json.load(open("credentials.json"))
APP_KEY = credentials["app_key"]
APP_SECRET = credentials["app_secret"]
OAUTH_TOKEN = credentials["oauth_token"]
OAUTH_TOKEN_SECRET = credentials["oauth_token_secret"]


twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    # Answers to be select from
    answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely", "you may rely on it",
               "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy, try again",
               "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
               "Don\'t count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful",
               "This is stupid"]
    while True:
        # Search for tweets that contain the required keyword
        search_results = twitter.search(q='@rags1390')
        filename = "tweetlist.txt"  # file which contains IDs of tweets it already replied to
        tweetlist = []
        with open(filename, 'r') as tweetfile:
            buff = tweetfile.readlines()
        for line in buff[:]:
            line = line.strip()
            print(line)
            tweetlist.append(line)
        try:
            for tweet in search_results["statuses"]:
                question = tweet["text"]
                question = question.lower()
                words = question.split(" ")
                # Check if  the ID of the result matches the already replied tweet. If already replied proceed. If not reply
                if tweet["id_str"] not in tweetlist:
                    print("not replied")
                    screenname = tweet["user"]["screen_name"]
                    # Check if the question contains "when","where","what","who","why". These questions generally do not have a Yes or No answer.
                    if "what" in words:
                        twitter.update_status(status="@" + screenname + " " + "Sorry I cannot answer that question. ",
                                              in_reply_to_status_id=tweet["id_str"])
                    elif "where" in words:
                        twitter.update_status(status="@" + screenname + " " + "Sorry I cannot answer that question. ",
                                              in_reply_to_status_id=tweet["id_str"])
                    elif "who" in words:
                        twitter.update_status(status="@" + screenname + " " + "Sorry I cannot answer that question. ",
                                              in_reply_to_status_id=tweet["id_str"])
                    elif "when" in words:
                        twitter.update_status(status="@" + screenname + " " + "Sorry I cannot answer that question. ",
                                              in_reply_to_status_id=tweet["id_str"])
                    elif "why" in words:
                        twitter.update_status(status="@" + screenname + " " + "I can only answer Yes or No questions ",
                                              in_reply_to_status_id=tweet["id_str"])
                    else:
                        twitter.update_status(status="@" + screenname + " " + random.choice(answers),
                                              in_reply_to_status_id=tweet["id_str"])
                    target = open(filename, 'a')
                    target.write(tweet["id_str"])
                    target.write("\n")
                    target.close()
                time.sleep(1)
        except TwythonError as a:
            print(a)
except TwythonError as e:
    print(e)
