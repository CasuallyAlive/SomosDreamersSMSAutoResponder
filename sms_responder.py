# Download the helper library from https://www.twilio.com/docs/python/install
import os
from flask import Flask, request
import pandas as pd
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

OPTIONS_PATH = "Resources/keywords_responses.txt"
HOST = "0.0.0.0"
PORT = 5000

options_dict = {}
# Load keywords and responses
with open(OPTIONS_PATH) as f:
    val = [line.strip() for line in f.readlines()]
    i = len(val) - 1

    for line in val:
        t = line.split(',')
        if t[0].lower() == "help":
            options_dict[t[0].lower()] = t[1]
        else:
            options_dict[t[0].lower()] = t[2]
            options_dict["help"] += f" Text '{t[0]}' for {t[1]}," if i > 0 else f" OR Text '{t[0]}' for {t[1]}."

        i-=1

# Setup web-app
auto_response_app = Flask(__name__)

@auto_response_app.route("/sms", methods=['Get', 'Post'])
def sms_auto_reply():
    # Get message from usr
    msg = request.values.get('Body', None)
    print(msg)
    # Split message into individual unique strings with whitespace
    msg_words = str(msg).lower().split()
    # dynamic response
    resp = MessagingResponse()
    for word in msg_words:
        print(word)
        if word in options_dict.keys():
            print(options_dict[word])
            resp.message(options_dict[word])
            return str(resp)
    
    resp.message("Thank you for reaching Somos Dreamer's automated SMS responder. Text 'HELP' for a complete list of our keywords!")
    return str(resp)


if __name__ == '__main__':
    auto_response_app.run(host=HOST, port=PORT)
