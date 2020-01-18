#!/usr/bin/env python3

import twitter
import requests
import subprocess as sp
import datetime, re
from datetime import time



def niceSoundingDate(date):
        dow = {"Mon":"monday",
               "Tue":"tuesday",
               "Wed":"wednesday",
               "Thu":"thursday",
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
        ordinals = ["first","second","third","fourth","fifth","sixth","seventh",
                    "eighth","ninth","tenth","eleventh","twelfth","thirteenth",
                    "fourteenth", "fifteenth","sixteenth","seventeenth",
                    "eighteenth","nineteenth","twentieth","twenty first",
                    "twenty second","twenty third", "twenty fourth",
                    "twenty fifth","twenty sixth","twenty seventh",
                    "twenty eighth","twenty ninth","thirtieth","thirty first"]


        date = date.split()
        date = date[0:3]
        date[0] = dow[date[0]]
        date[1] = month[date[1]]
        date[2] = ordinals[int(date[2])-1]
        return ' '.join(date)

def espeak(text, *args):
        print(args)
        args_list = ["espeak-ng"]
        if args:
                args_list.extend([text].extend(args))
        else:
                args_list.append(text)
        sp.run(args_list)

def delete_inaudibles(text):
        text_flags = [0]*len(text)
        # flag the urls in the text
        urls = tweet.urls
        for url in urls:
                indices = url.indices
                text_flags[indices[0]:indices[1]] = [1]*(indices[1]-indices[0])

        new_text = ''
        for i in range(len(text_flags)):
                if text_flags[i]==0:
                        new_text += text[i]
                else:
                        new_text += ' '
        return new_text
        
def audible_text(tweet):
        text = delete_audibles(tweet.full_text)
        # TODO: format text based on other properties of tweet object
        user_mentions = tweet.user_mentions
        for m in user_mentions:
                indices = m.indices
                
                

                
        
def greeting(date):
        ordinals = ["first","second","third","fourth","fifth","sixth","seventh",
                    "eighth","ninth","tenth","eleventh","twelfth","thirteenth",
                    "fourteenth", "fifteenth","sixteenth","seventeenth",
                    "eighteenth","nineteenth","twentieth","twenty first",
                    "twenty second","twenty third", "twenty fourth",
                    "twenty fifth","twenty sixth","twenty seventh",
                    "twenty eighth","twenty ninth","thirtieth","thirty first"]
        
        if date.minute == 0:
                minute = ""
        elif date.minute < 10:
                minute = "oh {}".format(date.minute)
        else:
                minute = date.minute

        dow = date.strftime('%A')
        month = date.strftime('%B')
        day = ordinals[date.day - 1]
        am_pm = date.strftime('%p')
        if date.hour < 12:
                greeting = "Good Morning!"
        elif date.hour < 18:
                greeting = "Good Afternoon!"
        else:
                greeting = "Good Evening!"

        hour = date.strftime('%I')
        if hour.startswith('0'): hour = hour[1]
        response = "{0} It is {1} {2} {3} on {4}, {5} {6}.".format(greeting, hour, minute, am_pm, dow, month, day)
        response = re.sub("\s\s+", " ", response)
        response += " Here are some recent tweets from your timeline"
        print(response)
       # espeak(response)

def date2int(date):
        return date.year*10000 + date.month*100 + date.day

def check_for_holiday(date):
        #TODO: check for holidays and append to greeting

def format_response(tweet):
        top_level_tweet_text = audible_text(tweet.full_text)
        if tweet.in_reply_to_status_id:
                original_tweet = api.GetStatus(tweet.in_reply_to_status_id)
                original_auth = original_tweet.user.name
                original_text = remove_http(original_tweet.full_text)
                response = "{} tweeted {}. ".format(original_auth,original_text)
                response += "To which {} replied: {}".format(tweet.user.name, top_level_tweet_text)
        elif tweet.quoted_status:
                quo_tweet = tweet.quoted_status
                quo_full_text = remove_http(quo_tweet.full_text)
                response = "{} quoted {}'s tweet that says {}. And then {} added {}.".format(tweet.user.name,quo_tweet.user.name,quo_full_text,top_level_tweet_text)
        elif tweet.retweeted_status:
                retweeted_text = remove_http(tweet.retweeted_status.full_text)
                response = "{} retweeted the following tweet by {}. {}".format(tweet.user.name, tweet.retweeted_status.user.name, retweeted_text)
        else:
                response = "{} tweeted {}".format(tweet.user.name, top_level_tweet_text)
        return response

def main(api):
        tweets = api.GetHomeTimeline(count=20, exclude_replies=True)
        cur_date = datetime.datetime.now()
        greeting(cur_date)
        # add one to current date so we ensure it will always get spoken first time thru for-loop
        cur_date = date2int(cur_date) + 1
        for tweet in tweets:
                tweet_date = date2int(datetime.date.fromtimestamp(tweet.created_at_in_seconds))
                if tweet_date < cur_date:
                        spk_date = niceSoundingDate(tweet.created_at)
                        # espeak(spk_date)
                        print(spk_date)
                        cur_date = tweet_date

                response = format_response(tweet)
                print(response)
                input("press any key to continue")
               # espeak(response)

if __name__ == "__main__":
        api = twitter.Api(consumer_key="Q6wIR9BVePrYP9pnF4rYWRGtn",
                          consumer_secret="cJJmc2blM6QVSjcaim3R5hDtqNOEHANZcn2iuVw8UrgA1etXX2",
                          access_token_key="1210385185692217345-juZyflHFepN7gemEjAxhKMoQespSg9",
                          access_token_secret="l0pDPKJSskdWZ2GZlMfB5GvoiO61ZksOhgO4Dvk09htuh",
                          tweet_mode='extended')
        
        main(api)
