# from gettext import gettext as _

# WELCOME_MESSAGE = _(
#     "Welcome, you can say Hello or Help. Which would you like to try?")
# HELLO_MSG = _("Hello Python World from Classes!")
# HELP_MSG = _("You can say hello to me! How can I help?")
# GOODBYE_MSG = _("Goodbye!")
# REFLECTOR_MSG = _("You just triggered {}")
# ERROR = _("Sorry, I had trouble doing what you asked. Please try again.")


text_responses = {
  "LaunchRequest" : {
                    "speech" : "In which city do you wanna party?",
                    "repromt" : "2004"
                    },
  "AMAZON.HelpIntent" : {
                    "speech" : "With this skill you can find raves by selecting a city and a date.",
                    "repromt" : "Just choose a city and a date and we will find an event for you"
                    },
  "AMAZON.StopIntent" : {
                    "speech" : "Bye, have a nice rave!",
                    "repromt" : ""
                    },
  "AMAZON.CancelIntent" : {
                    "speech" : "Bye, have a nice rave!",
                    "repromt" : ""
                    },
    "MyCityIntent" : {
                    "speech" : "Your city is {}. Now tell me the date!",
                    "repromt" : "Which city again?"
                    },
  "MyDateIntent" : {
                    "speech" : " add later",
                    "repromt" : "Which date again?"
                    },
  "PickShowIntent" : {
                    "speech" : "The lineup is {}. There are already {} attendants {} and the price is 10 Euro",
                    "repromt" : "On which event do you want to know more info?"
                    },
  "AMAZON.FallbackIntent" : {
                    "speech" : "I can not help you with that, tell me the city and the date",
                    "repromt" : "You can tell me city and date"
                    }

} 


def msg(intent_name, response_kind):

    if intent_name in text_responses:
        return text_responses[intent_name]['speech']
    else:
        return "No message available for this intent"



# class AlexaSpeechResposne:

#     def speech_msg(self, intent_name):

    
#     def repromt_msg(self, intent_name):
