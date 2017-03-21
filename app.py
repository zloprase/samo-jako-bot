# -*- coding: utf-8 -*-

#import bot
#print "done bot import"
#from bot import get_bot
#from chatterbot import ChatBot

import os
import sys
import json

import requests
from flask import Flask, request

print "done all imports"

app = Flask(__name__)

print "assigned flask to app"

initial_greeting = u'Ljubi čika! Samo šalji kratke poruke i bez sikiracije.'
greeting_messages = [
        'gde si',
        'sta ima',
        u'šta ima',
        'pozdrav',
    ]
greeting_answers = [
    initial_greeting
]
general_answers = [
    u'Ljubi čika!',
    'Samo bez sikiracije',
    'Ave Beli!',
    '#samojako',
    '#avebeli',
    'Samo Jako !',
]

answers = {
    'pare': u'Sve pare će da budu kod čike',
    'cika': u'Ljubi čika!',
    'ave': 'Ave Beli !',
    'ave 5': 'Ave Beli ! 5 !',
    '#samojako': '#samojako',
    'jako': 'Samo Jako !',
    'sikiracija': 'Samo bez sikiracije',
    '#avebeli': '#avebeli'
}

qa_dict = {
    'pare': answers['pare'],
    'kes': answers['pare'],
    'keš': answers['pare'],
    'lova': answers['pare'],
    'brinem': answers['sikiracija'],
    'sikiram': answers['sikiracija'],
    'sekiram': answers['sikiracija'],
    'mislim': answers['sikiracija'],
    'srce': answers['cika'],
    'cao': answers['cika'],
    'ćao': answers['cika'],
    'aj': answers['cika'],
    'vidimo se': answers['cika'],
    'pozdrav': answers['cika'],
    'ziveo': answers['ave'],
    'izbori': answers['ave 5'],
    'udri': answers['jako'],
    'rokaj': answers['jako'],
    'kako': answers['jako'],
    'mislim': answers['sikiracija'],
    'pobeda': answers['jako'],
    'jako': answers['jako'],
    '#samojako': answers['#avebeli'],
    '#avebeli': answers['#samojako'],
}


import distance
import random

def answer(message):
    count = 0

    smallest_distance = 999
    current_distance = smallest_distance
    closest_key = ""
    closest_word = ""

    for word in message.split():
        count += 1
        for key in qa_dict.keys():
            current_distance = distance.levenshtein(key, word)
            if current_distance < smallest_distance:
                closest_key = key
                closest_word = word
                smallest_distance = current_distance
        if count > 10 or smallest_distance < 2:
            print "no words in first 11 match - going random"
            closest_key = random.choice(qa_dict.keys())
            closest_word = ":( none found"
            break

    print "Nearest words are key '" + closest_key + \
          "' and word '" + closest_word + \
          "' with score " + str(smallest_distance) + "."

    return qa_dict[closest_key]




#bot = get_bot()
#bot.get_response("Ave Beli!")

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log_wrapper(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = "jako" if "text" not in messaging_event["message"] else messaging_event["message"]["text"] # the message's text

                    bot_reply =  answer(message_text) #bot.get_response(None)

                    send_message(sender_id, bot_reply)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log_wrapper("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log_wrapper(r.status_code)
        log_wrapper(r.text)


def log_wrapper(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    print "going into main"
    app.run(debug=True)

