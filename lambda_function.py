from bs4 import BeautifulSoup
import requests
import re
import json
import random


def lambda_handler(event, context):
	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])

def on_launch(launch_request, session):
	""" Called when the user launches the skill without specifying what they
	want
	"""
	# Dispatch to your skill's launch
	return get_welcome_response()
	

def on_intent(intent_request, session):
	
	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']
	
	# Dispatch to your skill's intent handlers
	if intent_name == "GetNewTravelQuoteIntent":
	    return get_random_quote()
	elif intent_name == "AMAZON.HelpIntent":
	    return get_welcome_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
	    return handle_session_end_request()
	else:
	    raise ValueError("Invalid intent")
	
def get_random_quote():
	
	quotes_list = []
	random_page = random.randint(1,30)
	url = "http://www.brainyquote.com/quotes/topics/travel_" + str(random_page)
	html = requests.get(url)
	soup = BeautifulSoup(html.text, "html.parser")
	quotes =  soup.find_all('a',attrs={"title":'view quote', "class":"oncl_q"})
	for quote in quotes:
		if(len(quote.text) != 0 and quote != None):
			quotes_list.append(quote.text)
	random_quote = random.choice(quotes_list)
	
	should_end_session = False
	response = {
	    'version': '1.0',
	    'response': {
	        'outputSpeech': {
	            'type': 'PlainText',
	            'text': random_quote
	        },
	        'should_end_session': should_end_session
	    }
	}
	
	return response
	
def get_welcome_response():
	
	speech_output = "Welcome to Travel Quotes. Please say tell me a quote or say exit"
	reprompt_output = "Please say tell me a quote or say exit"
	should_end_session = False
	response = {
	    'version': '1.0',
	    'response': {
	        'outputSpeech': {
	            'type': 'PlainText',
	            'text': speech_output,
	        },
	        'reprompt': {
	        	'outputSpeech': {
	            	'type': 'PlainText',
	            	'text': reprompt_output
	        	}
	    	},
	    	'shouldEndSession': should_end_session
	    }
	}
	return response

def handle_session_end_request():
	speech_output = "Thank you for trying Travel Quotes. " \
	                "Have a nice day! "
	# Setting this to true ends the session and exits the skill.
	should_end_session = True
	response = {
	    'version': '1.0',
	    'response': {
	        'outputSpeech': {
	            'type': 'PlainText',
	            'text': speech_output,
	        },
	        'reprompt': {
	            'outputSpeech': {
	                'type': 'PlainText',
	                'text': reprompt_output
	        	}
	    	},
	    	'shouldEndSession': should_end_session
	    }
	}
	return response