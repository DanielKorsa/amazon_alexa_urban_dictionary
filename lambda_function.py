# coding=utf-8

# Alexa - Urban Dictionary
# By Daniel Ko <gesundmeister@gmail.com>
# Alexa skill to interract with Urban Dictionary


# ------------------My Imports
import json
#import requests
#from bs4 import BeautifulSoup
from ud_scraper import word_of_the_day, random_word
from speech_responses_UD import msg

# -------------------Debugging
from datetime import datetime
 
# --------------------Imports from aws
import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import (
    is_request_type, is_intent_name, get_slot_value, request_util, 
    get_intent_name, get_request_type, get_dialog_state
)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard # Can delete
from ask_sdk_model import Response, DialogState
from ask_sdk_model.dialog import ElicitSlotDirective # For adding directives

#---------------- My variables---------
skill_name = "urban slang"
# city_slot = "city"
# city_slot_key = "CITY"
# show_n_slot_key = "SHOW NUMBER"

#TODO:
# Add word ratings 1 - 0
# Add ask a word meaning

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def intnt_name(handler_input):
    """
    Returns name of request or intent
    """
    req_type = get_request_type(handler_input)
    if req_type == "IntentRequest":
        return get_intent_name(handler_input)
    else:
        return req_type



@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    speech = msg(intent_name,'speech')
    reprompt = msg(intent_name,'reprompt')

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    speech = msg(intent_name,'speech')

    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response
    


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    speech = msg(intent_name,'speech')

    return handler_input.response_builder.speak(speech).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response



@sb.request_handler(can_handle_func=is_intent_name("WordOfTheDayIntent"))
def my_city_handler(handler_input):

    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    session_attr = handler_input.attributes_manager.session_attributes
    dialogue_state = get_dialog_state(handler_input)
    print('FUUUUCK its test' + str(dialogue_state))
    
    word = word_of_the_day()
    speech = word['word'] + word['meaning'] + word['example']

    # speech = msg(intent_name,'speech').format(current_city)
    reprompt = msg(intent_name,'reprompt')


    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("RandomWordIntent"))
def my_date_handler(handler_input):

    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    session_attr = handler_input.attributes_manager.session_attributes

    
    word = random_word()
    #speech = word['word'] + word['meaning'] + word['example']
    speech = msg(intent_name,'speech').format(word['word'], word['meaning'], word['example'])
    reprompt = msg(intent_name,'reprompt')

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response



@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    session_attr = handler_input.attributes_manager.session_attributes

    speech = ('ADD SPEACH HERE')
    reprompt = msg(intent_name,'reprompt')

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


def convert_speech_to_text(ssml_speech):
    """convert ssml speech to text, by removing html tags."""
    # type: (str) -> str
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


@sb.global_response_interceptor()
def add_card(handler_input, response):
    """Add a card by translating ssml text to card content."""
    # type: (HandlerInput, Response) -> None
    response.card = SimpleCard(
        title=skill_name,
        content=convert_speech_to_text(response.output_speech.ssml))


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Log response from alexa service."""
    # type: (HandlerInput, Response) -> None
    print("Alexa Response: {}\n".format(response))


@sb.global_request_interceptor()
def log_request(handler_input):
    """Log request to alexa service."""
    # type: (HandlerInput) -> None
    print("Alexa Request: {}\n".format(handler_input.request_envelope.request))


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> None
    print("Encountered following exception: {}".format(exception))

    speech = "Sorry, there was some problem. Lets try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


######## Convert SSML to Card text ############
# This is for automatic conversion of ssml to text content on simple card
# You can create your own simple cards for each response, if this is not
# what you want to use.

from six import PY2
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if not PY2:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)

################################################




handler = sb.lambda_handler() # Thats from Hello world example


