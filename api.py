from flask import Flask, render_template
import tweepy, time, sys
from time import sleep
from random import randint
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from flask import jsonify
from flask import request

app = Flask(__name__, template_folder="mytemplate")

# Keys
t_consumerkey= 'ONoYgdpRdkIj592dVQJi52Qsg'
t_secretkey= 'hn9y9Y7SBK5tiHWMVUKn6PRbUBUANjUX1aXcD9vwrpoTBFp8FJ'
access_tokenkey='846743565904564224-We0haZK8x9XomN18ITn9cSxqlYwouX5'
access_tokensecret='ValzlTvpS0Gq2SJAksUvvfyxm9N3a5o8dhSLJJrZzS6Ex'


#Authentication
auth = tweepy.OAuthHandler(t_consumerkey, t_secretkey)
auth.set_access_token(access_tokenkey, access_tokensecret)

api = tweepy.API(auth)

@app.route('/test')
def test():
	return "Test"

@app.route('/twitter')
def Go_bots():
	## take all arguments
	args = request.args
	article_links_array = args.getlist('article_links')
	hashtags_array = args.getlist('hashtags')
	macro_link = args['macro_link']
	tweet_text = args['tweet_text']
	
	#add counter for number of tweets
	counter = 2

	# create empty array
	search_result_article = []
	search_result_hashtag = []

	# search through twitter by article name
	for article in article_links_array:

		try:
			abc = api.search(article)
			search_result_article.append(abc)
		except Exception as e:
			print e

	
	# search through twitter by hastag
	for hashtag in hashtags_array:
		try:
			search_result_hashtag.append(api.search('#'+hashtag))
		except Exception as e:
			print e
			
	all_tweets_text = []

	return jsonify({"x": search_result_hashtag})
	
	#takes the name of the users tha tweets the articles and contacts them
	for tweets_a in search_result_article:
		for t in tweets_a:
			if counter ==0: 
			   break
			handle = "@" + t.user.screen_name
			m_a = handle + " " + macro_link
			all_tweets_text.append(m_a)
			s = api.update_status(m_a)
	#		nap = randint(1, 60)
			time.sleep(5)
			counter-=1
	# reset counter
	counter = 2
	
	#takes the name of the users tha tweets the hashtags and contacts them
	for tweets in search_result_hashtag:
		for tweet in tweets:
			if counter ==0: 
			   break
			handle = "@" + tweet.author.screen_name
			m = handle + " " + macro_link
			all_tweets_text.append(m)
			s = api.update_status(m)
	#		nap = randint(1, 60)
			time.sleep(5)
			counter-=1


	return jsonify({"tweets": all_tweets_text})



if(__name__) == '__main__':
    app.run(debug=True)
