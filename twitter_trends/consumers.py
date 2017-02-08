from channels import Group
from channels.sessions import channel_session
import json, tweepy, oauth2

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

@channel_session
def ws_connect(message):
	message.reply_channel.send({"accept": True})
	Group('twitter_trends-').add(message.reply_channel)

@channel_session
def ws_receive(message):

	if message.content['text'] == 'connected':
		print(True)
		trends = oauth_req( 'https://api.twitter.com/1.1/trends/place.json?id=1940345')
		Group('twitter_trends-').send({'text': str(trends)})
	else:
		tweets = tweet_stream( 'https://stream.twitter.com/1.1/statuses/filter.json?track='+message.content['text'],http_method="POST", post_body={'track':message.content['text']})
		Group('twitter_trends-').send({'text': str(trends)})


@channel_session
def ws_disconnect(message):
	Group('twitter_trends-').discard(message.reply_channel)

def oauth_req(url, http_method="GET", post_body='', http_headers=None):

	consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
	token = oauth2.Token(key=access_token, secret=access_token_secret)
	client = oauth2.Client(consumer, token)
	resp, content = client.request( url, method=http_method, body=post_body.encode('utf-8'), headers=http_headers )
	mjson =  json.loads((content.decode("unicode-escape"))[1:-1])
	return {'trends':mjson['trends'][0:25]}

def tweet_stream(url, http_method="POST", post_body='{\'track\'=\'dubai\'}', http_headers=None):

	consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
	token = oauth2.Token(key=access_token, secret=access_token_secret)
	client = oauth2.Client(consumer, token)
	resp, content = client.request( url, method=http_method, body=post_body.encode('utf-8'), headers=http_headers )
	mjson =  json.loads((content.decode("unicode-escape"))[1:-1])
	return {'tweets':mjson['tweets'][0:25]}