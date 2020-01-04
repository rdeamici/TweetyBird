import twitter
import requests

api = twitter.Api(consumer_key="Q6wIR9BVePrYP9pnF4rYWRGtn",
                  consumer_secret="cJJmc2blM6QVSjcaim3R5hDtqNOEHANZcn2iuVw8UrgA1etXX2",
                  access_token_key="1210385185692217345-juZyflHFepN7gemEjAxhKMoQespSg9",
                  access_token_secret="l0pDPKJSskdWZ2GZlMfB5GvoiO61ZksOhgO4Dvk09htuh",
		  tweet_mode='extended')

tweets = api.GetHomeTimeline(count=20, exclude_replies=True)

for tweet in tweets:
	if tweet.text:
		print("regular text = {}.\nlength of regular text = {}\n".format(tweet.text, len(tweet.text)))
	if tweet.full_text:
		print("full_text = {}.\nlength of full_text = {}.".format(tweet.full_text, len(tweet.full_text)))
	print("\n\n")

