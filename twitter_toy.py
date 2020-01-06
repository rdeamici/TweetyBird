#!/usr/bin/env python
import twitter
import requests
import subprocess as sp
import datetime, time
import num2words

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
        date[2] = num2words(date[2],to="ordinal")
        return ' '.join(date)

def espeak(text, *args):
        arg_list = ["espeak-ng"]
        if args is not None:   # TODO: look up way to join 2 lists 
                args_list.extend([text].extend(args))
        else:
                list_of_args.append(text)
        sp.run(list_of_args)

def create_greeting():
        cur_time = datetime.now()
        #TODO: fix this so it actually checks for proper time
        if cur_time.hour < 12:
                greeting = "Good Morning! "
        elif cur_time.hour < 18:
                greeting = "Good Afternoon! "
        elif cur_time < 24:
                greeting = "Good Evening! "
        return greeting+"Here are some recent tweets from your timeline."

def date2int(date):
        return date.year*10000 + date.month*100 + date.day

def main():
        api = twitter.Api(consumer_key="Q6wIR9BVePrYP9pnF4rYWRGtn",
                          consumer_secret="cJJmc2blM6QVSjcaim3R5hDtqNOEHANZcn2iuVw8UrgA1etXX2",
                          access_token_key="1210385185692217345-juZyflHFepN7gemEjAxhKMoQespSg9",
                          access_token_secret="l0pDPKJSskdWZ2GZlMfB5GvoiO61ZksOhgO4Dvk09htuh",
                          tweet_mode='extended')
        tweets = api.GetHomeTimeline(count=20, exclude_replies=True)
        greeting = create_greeting()
        espeak(greeting,args=None)
        cur_date = date2int(datetime.now) + 1
        for tweet in tweets:
                text = tweet.full_text
                user = tweet.user.name
                tweet_date = date2int(date.fromtimestamp(tweet.created_at_in_seconds))
                if tweet_date < cur_date:
                    spk_date = convert_date(tweet.created_at)
                    espeak(spk_date,args=None)
                    cur_date = tweet_date
                if tweet.in_reply_to_user_id:
                       replied_to =  # get user.name from user_id
                sp.run(['espeak-ng', 
        
if __name__ == "__name__":
        main()
