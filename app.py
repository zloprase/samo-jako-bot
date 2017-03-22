# -*- coding: cp1250 -*-

#import bot
#print "done bot import"
#from bot import get_bot
#from chatterbot import ChatBot

import json
import os
import sys
import traceback
from nltk.tokenize import word_tokenize

import requests
from flask import Flask, request

print "done all imports"

app = Flask(__name__)

print "assigned flask to app"

answers = {
    'pare': u'Sve pare će da budu kod čike',
    'cika': u'Ljubi čika!',
    'ave': 'Ave Beli !',
    '5': 'Ave Beli ! 5 !',
    '#samojako': '#samojako',
    'jako': 'Samo Jako !',
    'sikiracija': 'Samo bez sikiracije',
    '#avebeli': '#avebeli',
    'belo': 'Tvoje belo nije dovoljno belo',
    'bez': 'Bez sikiranja',
    'ima': u'Ima za čiku, al ima i za druge.',
    'rad': u'Radim od rane zore, već od 8.',
    'kobre': u'voleo bih da me čuvaju „kobre“ kad postanem predsednik.',
    'stan': u'Predsednik će živeti u vikendici u Mladenovcu',
    'vila': u'Vilu na Dedinju poklonićemo najboljim studentima.',
    'cilj': u'Glavni cilj je da se domognemo predsedničke pozicije, a posle ćemo da vidimo.',
    'tajkun': u'Ljubišin tajkun je kum Petar Popović Ajkula',
    'sarma': u'Sarmu probo nisi.',
    'mrak': u'Šta se beli u mraku Srbije?',
    'glava': u'Samo jako uzdignute glave !',
    'doktorat': u'Idem po doktorat u korporativnom industrijskom menadžmentu, jer to je budućnost.',
    'placenik': u'Idem na obuku za strane plaćenike, a dogovaramo i sastanak sa Trampom',
    'sumadija': u'Tokom programa biće obavljeni i važni razgovori o potencijalnim ulaganjima naše dijaspore u AP Šumadija',
    'zena': u'Kad postanem preCednik, ni jedna žena ne sme biti izvređana.',
    'predskazan': u'Beli je predskazan ...',
    'prevaren': u'Da li je bilo ko od vas 12,640 kad je potpisao bio prevaren i nije znao da podržava Ljubišu Preletačevića Belog?',
    'rik': u'Žao mi je što ste zabrinuti i ne verujete RIK-u.',
    'zemun': u'Znači uspeo sam da ispoštujem Zemun. Ispoštujte i vi brata. ',
    'sirotinja': u'Sirotinja uzvraća udarac',
    'mart': u'Žene moje srećan osmi mart. Ljubi čika šišarkice',
    'bot': u'Evo ponude: moji botovi početnici imaju jagnjetinu. Moguće napredovanje.',
    'paypal': u'PayPal account je  belisamojako@gmail.com  ',
    'saj': u'Došli i SAJevci da pomognu skupljanje potpisa po Mladenovcu',
    'formula': u'Moja formula je jednostavna. Znači samo jako i bez sikiranja, biće sve ok. ;)',
    'godina': u'Da završimo ovu godinu pa da krenemo Samo Jako u narednu !',
    'interes': u'Ja gledam da imam svoj lični interes, ali da dam i narodu. Suština je da ću krasti, da ću se vajditi, ali i da ću dati narodu. Tako treba raditi i tako smo namireni i mi i oni',
    'soros': u'Ko da više love, taj je dobrodošao. Nebitno je ko finansira. Ko je spreman da uloži novac u nešto što je dobro, taj je dobrodošao.',
    'glasanje': u'Treba da izađete na izbore, jako je bitno. Dosta ste sedeli kući, ništa niste radili. Suština je da sada uradite nešto novo i bitno, izađite 2. aprila na izbore i zaokružite broj pet – ; Ljubiša Preletačević Beli. Ljubi čika, bez sikiranje',
    'kosovo': u'Izvolite, možete da se vratite, ne samo vi, već i Bugarska, Grčka… Od Mađarske do Grčke da se svi ujedinimo',
    'mmf': u'Ne znam ko to drži. Lepo ‘out’, izlaziš iz zemlje, a sva lova kod ‘čike’. Narod zna da je lova kod mene, treba ti nešto, dođeš kod mene, pitaš treba mi za to i to, ja iskeširam sve iz džepa, odem provjerim da li si to uradio i lijepo',
    'ljubi': u'Ljubi čika, bez sikiranja',
    'loto': u'Loto je čika Beli namestio. Dosta su drugi nameštali loto, sad malo čika. Da usrećim kojeg Mladenovčanina, biće toga još. Ljubi predsednik.',
    'istokzapad': u'Radim za zapad i za istok. U zavisnosti kuda više love, ja za njih radim, tako da je kod mene sve to promenljivo.',
    'kontrola': u'Nema tu kontrole, znači, mojih botova ima mnogo više od ostalih stranaka i tu nema neke preterane kontrole, podelimo im te kaprićoze i oni se malo smire, ali opet krenu, mnogo su jaki, ko god krene na mene, oni me brane.',
    'krug': u'Sad idemo u krug, sad malo ja deset godina, pa će neko drugi. Nema tu neke filozofije, razumeš.',
    'iskreno': u'Pa znaš šta je fora, što bih ja ujedinio sve ljude. Svi da se volimo, da se grlimo, da nam bude svima lepo, da ne postoje granice, da nema NATO-a, i to je ono iskreno.',
    'drugi': u'Nema ništa od toga, prvi krug ja dobijam i to je to.',
    'dama': u' Postoji prva dama. Mislim ona nije još prva dama, ja kada postanem prvi predsednik, onda ću je uzeti za ženu.',
    'zelenas': u'Nema tu kancelarije, ti dođeš kod mene lično, tražiš od mene pare. Znači nema ti da tražiš ni od koga drugog, pare će da budu kod mene kući, ti dođeš kod mene pa tražiš pare. Sad, ti si seljak čovek hoćeš da poseješ njivu neku tamo, kupiš kombajn, dođeš kod mene i tražiš, ja odem posle i proverim jesi li kupio i to je to. To je prosto.',
    'jezik': u'Dakle engleski, nemački, francuski.',
    'veselje': u'Napraviću opšte narodno veselje. Napravićemo 20 mangala za 20 bravova i opšte narodno veselje da proslavimo predsednikovu pobedu, onako narodski što se kaže.',
    'nikolic': u'Pa verovatno bolje igram od Nikolica, imam smisla za igranku, žene kažu da sam zgodan, tako da, za početak, i tri strana jezika, a spreman sam da naučim još dva, mislim da je to za početak dovoljno.',
    'kruna': u'Verovatno ću imati prilike da upoznam predsednika kad bude predaja kruna.',
    'tempo': u'Evo ja ti prijatelju radim od 7 jutros, pa ti vidi sad koliko je to, znači mogu da izguram 22 sata da radim.',
    'arapi': u'Kad postanem predsednik neću da radim ništa, šta ima da radim, da potpisujem tamo, da igram sa Arapima, da pečem rakiju, da se šetam ambasadama. Sad da izguram ovo po 22 sata da radim i posle milina Božija.',
    'istina': u'Kako neće, ljudima treba istina, niko nije bio iskren 20-30 godina, ja izađem i kažem, kao što sam tebi rekao malopre, moj lični interes je na prvom mestu, pa onda drugi, ali ja ću davati i njima.',
    'srdja': u'Ja sam išao na privatne časove kod Srđe, 1000 dinara po času je bilo i uz to mi je matematiku predavao, jedan od koeficijenata je 2, to ti je dovoljno da budeš predsednik države. Tako da to je sve po tom principtu.',
    'kabinet': u'Vidiš da ja širim ljubav, nema haosa. Ja ne želim ljude na ulici, želim sebe u predsedničkom kabinetu.',
    'lgbt': u'To je ono što ti kažem, znači ako je potrebno i to da se uradi samo da ja postanem predsednik, nije nikakav problem. Što se mene tiče mogu goli ljudi da šetaju ulicama, ako ću ja da budem presednik države. Samo za taj lični interes, šta god, treba da se uradi. Samo da se dođe do cilja.',
    'ujedini': u'Pa ja bih potpisao da se ujedinimo svi komplet od Mađarske dole do Grčke. Sve ako može da se to ujedini u jednu zemlju, bez razmišljanja. Niko da se ne otcepljuje.',
    'golf': u'Golf „dvica“, 1.6 td, 86. godište, znači jednom mi je nestalo goriva dole na primorju sipao sam karton zejtina, je li veruješ da je dogurao do Beograda?',
    'referendum': u'Ko više nudi love, prijatelju, tamo treba da idemo. Sad da li to bila Evropska unija ili unija Azije i Severne Koreje, to je nebitno. Ja to kažem, da ne bude da je moje mišljenje, referendum pa nek narod odluči. Pošteno.',
    'jeremic': u'Divan momak, stvarno legendica, divan dečak, radi svoj posao kako treba.',
    'jankovic': u'Fin momak i Saša je stvarno fin dečak. On je bio beše zaštitnik građana, to nije loša funkcija.',
    'radulovic': u'Oduševio me čovek što je pozivao da ljudi potpišu za nas, hvala mu za to.',
    'bosko': u'Boško je momak i po. Ne pratim nešto njegove političke aktivnosti, ali ovako je stvarno fin čovek.',
    'gandalf': u'Gandalf Beli. Rekao je Tarabić da će da dođe čovek na belom konju, ne znam da li je rekao u belom odelu. Ali belo kao čisto nešto je prepoznatljivo.',
    'preletacevic': u'Nijedan se ne preziva Preletačević osim mene. Ja opet u svom prezimenu imam iskrenost, razumeš, ja kažem da sam Preletačević. To je suština.',
}

qa_dict = {
    'pare': answers['pare'],
    'kes': answers['pare'],
    u'keš': answers['pare'],
    'lova': answers['pare'],
    'brinem': answers['sikiracija'],
    'sikiram': answers['sikiracija'],
    'sekiram': answers['sikiracija'],
    'mislim': answers['sikiracija'],
    'srce': answers['ljubi'],
    'cao': answers['ljubi'],
    u'ćao': answers['cika'],
    'ajd': answers['cika'],
    'vidimo se': answers['cika'],
    'pozdrav': answers['ljubi'],
    'ziveo': answers['ave'],
    'izbori': answers['5'],
    'udri': answers['jako'],
    'rokaj': answers['jako'],
    'kako': answers['jako'],
    'pobeda': answers['jako'],
    'jako': answers['jako'],
    '#samojako': answers['#avebeli'],
    '#avebeli': answers['#samojako'],
    'belo': answers['belo'],
    'odelo': answers['belo'],
    'bez': answers['bez'],
    'pet': answers['5'],
    '5eli': answers['5'],
    'ave': answers['#avebeli'],
    'ima': answers['ima'],
    'ljubim': answers['cika'],
    'rad': answers['rad'],
    'kobra': answers['kobre'],
    'zmija': answers['kobre'],
    'poskok': answers['kobre'],
    'stan': answers['stan'],
    'kuca': answers['stan'],
    'vila': answers['vila'],
    'dedinje': answers['vila'],
    'student': answers['vila'],
    'cilj': answers['cilj'],
    'posle': answers['cilj'],
    'tajkun': answers['tajkun'],
    'placenik': answers['placenik'],
    'ajkula': answers['tajkun'],
    'sarma': answers['sarma'],
    'spn': answers['sarma'],
    'glava': answers['glava'],
    'doktorat': answers['doktorat'],
    'diploma': answers['doktorat'],
    'izdajnik': answers['placenik'],
    'sumadija': answers['sumadija'],
    'zena': answers['zena'],
    'predskazan': answers['predskazan'],
    'proreknut': answers['predskazan'],
    'tarot': answers['predskazan'],
    'sudbina': answers['predskazan'],
    'potpisi': answers['prevaren'],
    'prevara': answers['prevaren'],
    'podrska': answers['prevaren'],
    'rik': answers['rik'],
    'zabrinut': answers['sikiracija'],
    'zemun': answers['zemun'],
    'munze': answers['zemun'],
    'sirotinja': answers['sirotinja'],
    'siromah': answers['sirotinja'],
    'leba': answers['sirotinja'],
    'mart': answers['mart'],
    'bot': answers['bot'],
    'botovi': answers['bot'],
    'paypal': answers['paypal'],
    'uplata': answers['paypal'],
    'saj': answers['saj'],
    'formula': answers['formula'],
    'recept': answers['formula'],
    'godina': answers['godina'],
    'interes': answers['interes'],
    'kradja': answers['interes'],
    'vajda': answers['interes'],
    'ovajdi': answers['interes'],
    'soros': answers['soros'],
    'finansira': answers['soros'],
    'glasa': answers['glasanje'],
    'izbor': answers['glasanje'],
    'zaokruzi': answers['glasanje'],
    'kosovo': answers['kosovo'],
    'mmf': answers['mmf'],
    'monetarni': answers['mmf'],
    'kredit': answers['mmf'],
    'pozajmica': answers['mmf'],
    'pozajmi': answers['mmf'],
    'dug': answers['mmf'],
    'dugovanja': answers['mmf'],
    'loto': answers['loto'],
    'lutrija': answers['loto'],
    'istok': answers['istokzapad'],
    'zapad': answers['istokzapad'],
    u'radiš': answers['rad'],
    'jutro': answers['rad'],
    'komunist': answers['istokzapad'],
    'stranci': answers['istokzapad'],
    'kontrola': answers['kontrola'],
    'pica': answers['bot'],
    'sendvic': answers['bot'],
    'krug': answers['krug'],
    'organizacija': answers['kontrola'],
    'filozofija': answers['krug'],
    'ujedinio': answers['iskreno'],
    'iskreno': answers['iskreno'],
    'nato': answers['iskreno'],
    'alijansa': answers['iskreno'],
    'drugi': answers['drugi'],
    'dama': answers['dama'],
    u'ženidba': answers['dama'],
    'zenidba': answers['dama'],
    'zene': answers['dama'],
    'devojku': answers['dama'],
    'ozeni': answers['dama'],
    u'ženiš': answers['dama'],
    'zenis': answers['dama'],
    'zelenas': answers['zelenas'],
    'njivu': answers['zelenas'],
    'kombajn': answers['zelenas'],
    'jezik': answers['jezik'],
    'engleski': answers['jezik'],
    'nemacki': answers['jezik'],
    'francuski': answers['jezik'],
    'veselje': answers['veselje'],
    'pobede': answers['veselje'],
    'slavlje': answers['veselje'],
    'proslava': answers['veselje'],
    'nikolic': answers['nikolic'],
    u'nikolić': answers['nikolic'],
    'kruna': answers['kruna'],
    'predsednik': answers['kruna'],
    'tempo': answers['tempo'],
    'jutros': answers['tempo'],
    'ustao': answers['tempo'],
    'rano': answers['tempo'],
    'arapi': answers['arapi'],
    'rakiju': answers['arapi'],
    'ambasada': answers['arapi'],
    'istina': answers['istina'],
    'srdja': answers['srdja'],
    u'srđa': answers['srdja'],
    'casovi': answers['srdja'],
    u'časovi': answers['srdja'],
    u'uči': answers['srdja'],
    'haos': answers['kabinet'],
    'ulici': answers['kabinet'],
    'ljubav': answers['kabinet'],
    'lgbt': answers['lgbt'],
    'parada': answers['lgbt'],
    'prajd': answers['lgbt'],
    'ujedini': answers['ujedini'],
    'ujedinimo': answers['ujedini'],
    'golf': answers['golf'],
    'auto': answers['golf'],
    'kola': answers['golf'],
    'aktivisti': answers['bot'],
    'referendum': answers['referendum'],
    'glasanje': answers['referendum'],
    u'odluči': answers['referendum'],
    'odluci': answers['referendum'],
    'unija': answers['referendum'],
    'jeremic': answers['jeremic'],
    'vuk': answers['jeremic'],
    'jankovic': answers['jankovic'],
    'radulovic': answers['radulovic'],
    'bosko': answers['bosko'],
    'obradovic': answers['bosko'],
    'gandalf': answers['gandalf'],
    u'tarabić': answers['gandalf'],
    'preletacevic': answers['preletacevic'],
    u'preletačević': answers['preletacevic']
}


import distance
def answer(message):
    message = message.lower()
    try:
        count = 0
        smallest_distance = 999
        closest_key = ""
        closest_word = ""

        for word in word_tokenize(message):
            count += 1
            if len(word) < 3 or word == 'beli':
                continue

            for key in qa_dict.keys():
                #print "key: " + key
                #print "word: " + word
                current_distance = distance.levenshtein(key, word)
                #print "distance: " + str(current_distance)
                if current_distance < smallest_distance:
                    closest_key = key
                    closest_word = word
                    smallest_distance = current_distance
            if count > 10:
                #print 1
                #log_wrapper("no words in first 11 match - going for the best one")
                break
            if smallest_distance < 2:
                #print 2
                #log_wrapper("found the best one after " + str(count) + " tries." )
                break

        log_wrapper("Nearest words are key '" + closest_key + \
              "' and word '" + closest_word + \
              "' with score " + str(smallest_distance) + ".")

        return qa_dict[closest_key]
    except:
        log_wrapper(traceback.print_exc())
        return "#samojakobot"


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
                    try:
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = "jako" if "text" not in messaging_event["message"] else messaging_event["message"]["text"] # the message's text

                        bot_reply =  answer(message_text)

                        #log_wrapper(bot_reply)

                        send_message(sender_id, bot_reply.decode('utf8'))
                    except:
                        log_wrapper("Could not answer due to error")
                        log_wrapper(traceback.print_exc())

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
    print "Going into main"
    app.run(debug=False)

