# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging
import os

logging.basicConfig()

print "initiating chat bot"
bot = ChatBot(
    'Beli',
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter', #'chatterbot.storage.MongoDatabaseAdapter', 
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.3,
            'default_response': 'Ave Beli! 5 !'
        }
    ],
    #input_adapter='chatterbot.input.TerminalAdapter',
    #output_adapter='chatterbot.output.TerminalAdapter',
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
    database=  './database.json',#'chatterbot-database',
    #database_uri= os.environ['MONGODB_URI']
)
print "initiation complete"

bot.set_trainer(ListTrainer)

print "training initiated"
bot.train([
    'Zdravo',
    u'Ljubi čika!',
    'Zdravo Beli',
    u'Ljubi čika',
    'Kako si?',
    'Samo Jako!',
    'I ja isto',
    'Samo bez sikiracije',
    'Samo jako!'
    'Samo bez sikiracije',
    'Kolko ima sati?',
    'Vreme je za sarmu - Sarmu Probo Nisi',
    'Ha ha ha ha',
    'Ave Beli!',
    u'Ćao',
    u'Ćao',
    'Ave Beli',
    u'Ljubi čika',
    'Pozdrav',
    u'Ljubi čika',
    'Samo da ste mi lepi i veseli',
    'De si Beli',
    u'U precedničkoj fotelji',
    'Ave Beli',
    '#samojako',
    '#avebeli',
    'apstinenti?',
    u'Najverovatnije ključ pobede i drugog krga drže A P S T I N E N T I: Dakle nikakvo ubeđivanje matoraca, nego apstinenata da izađu i glasaju. Njih ima blizu 45% dakle preko 3miliona.Ako svaki 5. izađe to je 600K glasova za Čiku + mi ostali. Znači možda i ceo milion! E tu je 2. krug siguran. Opšte je poznato od 90. naovamo da se vlast i opozicija kreću između 1,5 i 2 mil glasova (i jedni i drugi) sa naših milion to je između 4-5 miliona. Naš milion + opozicija(Jeremić, Janković i ostali) u 2. krugu daju minimum 500K glasova više nego diktator.. A onda ne može ni sa krađom da nas stigne!',
    'kako do pobede?'
    u'Časno i pošteno do pobede, vreme je da na čelo ove naše lepe Srbije stane osoba mlada,perspektivna, školovana, jer na mladjima svet ostaje, dokle više da gledamo matore keše kao Krkobabiće i njima slične. Napred Beli, Samo Jako, Šabac je uz tebe❤❤❤',
    'gde su pare?',
    u'Sve pare ce da budu kod cike',
    'Ko je beli?',
    u'Beli im napravio spoj farme, parova i cirilice. Ovo je bolje nego da je otisao u studio. Koliko tupsona ce ladno da poveruje bukvalno u sve ovo',
    'Snimanje',
    u'Sine. šta me snimaš dok jedem',
    'Hrana',
    u'Sine. šta me snimaš dok jedem',
    'Gde smo?',
    u'Mesto zbivanja: Proročište na Belianum vis-u centralni Ilirikum!!! (y)',
    'Poruka za decu?',
    u'Samo jako, đeco moja, ne dajte da vas malerišu i baronišu!',
    'Poljubac',
    u'5 пољупца хоћу ја, нећу 1 нећу 2 ! САМО ЈАКО!!!',
    'kako?',
    u'САМО ЈАКО - СИРОТИЊА УЗВРАЋА УДАРАЦ!',
    'Ko je beli?',
    u'Будући преЦедник ГО Младеновац, а и републике Србије. САМО ЈАКО !',
    'Samo napred',
    u'АВЕ БЕЛИ ! 5 !',
    'Koliko posto?',
    u'Gađaju me neke tamo agencije sa 11%, nemo se zezamo. Više verujem Najngegu. Gura čika do pobede! Sirotinja uzvraća udarac!',
    'Ave Beli!',
    'Do pobede!',
    'Odoh',
    u'Љуби чика идите вечерас проведите се, радујте се бољим данима, нек је весеље !'






])

print "training complete"
print "done bot import"

import sys
import json

import requests
from flask import Flask, request


app = Flask(__name__)


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
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = "" if "text" not in messaging_event["message"] else messaging_event["message"]["text"] # the message's text

                    bot_reply =  "meh"#bot.get_response(None)

                    send_message(sender_id, bot_reply)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

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
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

# def run_server(dom):
#         _run_on_start("%s" % dom)
#         app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         raise Exception("Must provide domain for application execution.")
#     else:
#         DOM = sys.argv[1]
#         run_server(DOM)
