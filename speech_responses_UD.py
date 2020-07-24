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
                    "speech" : 'Booyakasha, you can learn a word of the day or a random word.',
                    "repromt" : "For real, wanna learn some slang from the streets?"
                    },
  "AMAZON.HelpIntent" : {
                    "speech" : "You can choose between a word of the day, or a random word",
                    "repromt" : "For example, say random word, and you will get its meaning and an example"
                    },
  "AMAZON.StopIntent" : {
                    "speech" : "Bye, keep it real",
                    "repromt" : ""
                    },
  "AMAZON.CancelIntent" : {
                    "speech" : "Respek, knowledge is power",
                    "repromt" : ""
                    },
    "RandomWordIntent" : {
                    "speech" : "{}. Here is the meaning: {}. <break time='1s'/>  Example: {}",
                    "repromt" : "Which city again?"
                    },
  "WordOfTheDayIntent" : {
                    "speech" : " add later",
                    "repromt" : "Which date again?"
                    },
  "TEMPLATE" : {
                    "speech" : "",
                    "repromt" : ""
                    },
  "AMAZON.FallbackIntent" : {
                    "speech" : "For real, just ask for a random word",
                    "repromt" : "Wicked, want another word?"
                    }

} 



def msg(intent_name, response_kind, emotion = "excited", intensity = "high"):

    if intent_name in text_responses:
        
        return '<amazon:emotion name={} intensity={}>{}</amazon:emotion>"'.format(emotion, intensity,text_responses[intent_name]['speech'])
    else:
        return "No message available for this intent"


# class AlexaSpeechResposne:

#     def speech_msg(self, intent_name):

    
#     def repromt_msg(self, intent_name):

#print(msg('LaunchRequest', 'speech'))

