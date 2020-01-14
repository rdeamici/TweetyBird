#!/usr/bin/env python3

import twitter
import requests
import subprocess as sp
import datetime
from datetime import time
from num2words import num2words

def convert_date(date):
        dow = {"Mon":"monday",
               "Tues":"tuesday",
               "Wed":"wednesday",
               "Thurs":"thursday",
               "Fri":"friday",
               "Sat":"saturday",
               "Sun":"sunday"}
        month = {"Jan":"january",
                 "Feb":"february",
                 "Mar":"march",
                 "Apr":"april",
                 "Jun":"june",
                 "Jul":"july",
                 "Aug":"august",
                 "Sep":"septmber",
                 "Oct":"october",
                 "Nov":"november",
                 "Dec":"december"}

        date = date.split()
        date = date[:3]
        date[0] = dow[date[0]]
        date[1] = month[date[1]]
        date[2] = num2words(date[2],to='ordinal')
        return ' '.join(date)

def espeak(text, *args):
        print(args)
        args_list = ["espeak-ng"]
        if args:
                args_list.extend([text].extend(args))
        else:
                args_list.append(text)
        sp.run(args_list)

def greeting(date):
        if date.hour < 12:
                greeting = "Good Morning! "
        elif date.hour < 18:
                greeting = "Good Afternoon! "
        elif date.hour < 24:
                greeting = "Good Evening! "
        espeak(greeting+"Here are some recent tweets from your timeline.")

def date2int(date):
        return date.year*10000 + date.month*100 + date.day

def format_response(tweet):
        if tweet.in_reply_to_status_id:
                original_tweet = api.getStatus(tweet.in_reply_to_status_id)
                original_auth = original_tweet.user.name
                original_text = original_tweet.full_text
                response = "{} tweeted {}. ".format(original_tweet,original_text)
                response += "To which {} replied: {}".format(tweet.user.name, tweet.full_text)
        elif tweet.quoted_status:
                quoted_tweet = tweet.quoted_status
                response = "{}'s tweet saying {} was quoted by {}, adding {}.".format(quoted_tweet.user.name, quoted_tweet.full_text, tweet.user.name, tweet.full_text)
        elif tweet.retweeted_status:
                response = "{} retweeted the following tweet by {}. {}".format(tweet.user.name, tweet.retweeted_status.user.name, tweet.retweeted_status.full_text)
        else:
                response = "{} tweeted {}".format(tweet.user.name, tweet.full_text)
        return response

def main(api):
        tweets = api.GetHomeTimeline(count=20, exclude_replies=True)
        cur_date = datetime.datetime.now()
        greeting(cur_date)
        comparable_date = date2int(cur_date)
        cur_date += 1
        for tweet in tweets:
                tweet_date = date2int(datetime.date.fromtimestamp(tweet.created_at_in_seconds))
                if tweet_date < cur_date:
                        spk_date = convert_date(tweet.created_at)
                        espeak(spk_date)
                        cur_date = tweet_date

                response = format_response(tweet)
                espeak(response)

if __name__ == "__main__":
        api = twitter.Api(consumer_key="Q6wIR9BVePrYP9pnF4rYWRGtn",
                          consumer_secret="cJJmc2blM6QVSjcaim3R5hDtqNOEHANZcn2iuVw8UrgA1etXX2",
                          access_token_key="1210385185692217345-juZyflHFepN7gemEjAxhKMoQespSg9",
                          access_token_secret="l0pDPKJSskdWZ2GZlMfB5GvoiO61ZksOhgO4Dvk09htuh",
                          tweet_mode='extended')
        
        main(api)
