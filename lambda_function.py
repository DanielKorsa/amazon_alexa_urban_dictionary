# coding=utf-8

# Alexa - Urban Dictionary
# By Danil Konovalov <gesundmeister@gmail.com>
# Alexa skill to interract with Urban Dictionary


# ------------------My Imports
import json
import requests
from bs4 import BeautifulSoup
from ud_scraper import main
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

# --------------------------------------
#---------------- My variables---------
city_slot = "city"
date_slot = "date"
show_n_slot = "show_number"
# Slot attribute keys
city_slot_key = "CITY"
date_slot_key = "DATE"
show_n_slot_key = "SHOW NUMBER"
shows_list_key = "SHOWS LIST"
help_text = "ADD IT to file"
skill_name = "resident advisor"
#-------------------------------

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#handler_input.response_builder.set_should_end_session(False)
#session_attr = handler_input.attributes_manager.session_attributes
def intnt_name(handler_input):
    """ Return str
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

    handler_input.response_builder.speak(speech).ask(help_text)
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


    #---- Choose City Slot-------------------------------------------

@sb.request_handler(can_handle_func=is_intent_name("MyCityIntent"))
def my_city_handler(handler_input):

    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    session_attr = handler_input.attributes_manager.session_attributes
    dialogue_state = get_dialog_state(handler_input)
    print('FUUUUCK' + str(dialogue_state))

    current_city = get_slot_value(handler_input, city_slot)
    session_attr[city_slot_key] = current_city # save city in current sesh
    
    speech = msg(intent_name,'speech').format(current_city)
    reprompt = msg(intent_name,'reprompt')

    # speech = "I'm not sure what your favorite city is, please try again"
    # reprompt = ("I'm not sure what your party city is. ")

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response

    #---- Choose DATE Slot-------------------------------------------

@sb.request_handler(can_handle_func=is_intent_name("MyDateIntent"))
def my_date_handler(handler_input):

    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    session_attr = handler_input.attributes_manager.session_attributes

    current_date = get_slot_value(handler_input, date_slot)
    session_attr[date_slot_key] = current_date # save date in current sesh
    
    if city_slot_key in session_attr:
        current_city = session_attr[city_slot_key] # Get city name from attributes
    else:
        print("ERROR: CITY WAS NOT SAVED BEFORE")


    shows, shows_msg = main(current_date, current_city) # Get list of shows 
    session_attr[shows_list_key] = shows # save list of shows in Session Attributes
    
    speech = (shows_msg)
    reprompt = msg(intent_name,'reprompt')
    # speech = "I'm not sure when you want to party, please try again."
    # reprompt = ("When do you want to party? ")

    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response

    #---- Choose SHOW Slot-------------------------------------------

@sb.request_handler(can_handle_func=is_intent_name("PickShowIntent"))
def pcik_shows_handler(handler_input):

    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    session_attr = handler_input.attributes_manager.session_attributes
    
    show_n = int(get_slot_value(handler_input, show_n_slot)) # get show number
    #print("SHOW NUMBER type is {}".format(type(show_n)))

    if shows_list_key in session_attr:
        shows_list = session_attr[shows_list_key]
        picked_show = shows_list[show_n -1] # User will say First and list is 0 based
    else:
        picked_show = 'NO SHOWS SAVED IN ATTRIBUTES'
    

    speech = msg(intent_name,'speech').format(picked_show['lineup'],picked_show['attending'],picked_show['venue'])
    reprompt = msg(intent_name,'reprompt')
    print(speech)
    # directive=ElicitSlotDirective(
    #     updated_intent=Intent(
    #         name="FavoriteColorIntent"), 
    #     slot_to_elicit="favoriteColor"))


    handler_input.response_builder.speak(speech).ask(reprompt)#.add_directive(directive)
    return handler_input.response_builder.response

    #---- Choose SHOW Slot---------------------------------------------


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    intent_name = intnt_name(handler_input)
    session_attr = handler_input.attributes_manager.session_attributes

    speech = (shows_msg)
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




# def get_intent_name(handler_input):
#     return ask_sdk_core.utils.request_util.get_intent_name(handler_input)


# def my_func(handler_input):
# 	# type: (HandlerInput) -> bool
# 	return (is_intent_name("PetMatchIntent")(handler_input) 
# 		and handler_input.request_envelope.request.dialog_state != DialogState.COMPLETED)
 
# @sb.request_handler(can_handle_func=my_func)
# def my_intent_handler(handler_input):
# 	# Do your normal intent processing here