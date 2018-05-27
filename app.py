#Python libraries that we need to import for our bot
import requests
from PIL import Image
import json
import time
from selenium import webdriver
from flask import Flask, request
from requests_toolbelt import MultipartEncoder
from pymessenger.bot import Bot
import os
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN'] #EAAZAm0NGhNvoBABPn6MhEJGxN2Hhw37GZC53iXBOUDqGEbHsPV03ZCZCHSWnaW5y4q8a1H2gb5SC8VNKQKnfvMV0ucD03cPaeDnnovXzibahv6SapNJOWQd10UvG1sO0TtW4qE3kFx652tzLeA1tOh12xoZBZA4qo6uPsXTTIZCfAZDZD
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)
#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    commande0 ='XXX'
    print('Initialisation')
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        print('Vérification du token !')
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the
        #time.sleep(5)
        try:
            output = request.get_json()
            event = output['entry'][-1]
        except:
            print('Erreur de requete')
        else:
            try:
                message = event['messaging'][-1]
                recipient_id = message['sender']['id']
                commande = message['message']['text']
            except:
                print('Message non pris en compte')
            else:
                print(recipient_id+' a envoyé : '+commande+''' à l'instant : '''+str(message['timestamp']))
                if message['message'].get('text') and "Mirmoc" in message['message']['text'] and commande != commande0 :
                    commande0 = commande
                    try:
                        scraping(commande,recipient_id)
                        send_report(recipient_id)
                    except:
                        print('Erreur')
                        bot.send_text_message(recipient_id,'''Désolé, je n'ai pas compris. Je ne connais que les spots 'Seignosse', 'Siouville', 'La_torche', 'Vendee', 'Quiberon' et 'Etretat'. Je ne comprends que la syntaxe 'Mirmoc spot' ''')
                else:
                    bot.send_text_message(recipient_id,'''Désolé, je n'ai pas compris. Je ne connais que les spots 'Seignosse', 'Siouville', 'La_torche', 'Vendee', 'Quiberon' et 'Etretat'. Je ne comprends que la syntaxe 'Mirmoc spot' ''')
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def scraping(commande,recipient_id):
    url = {'Quiberon' :
        {'surf_report' : "https://www.surf-report.com/meteo-surf/sainte-barbe-s1169.html",
         'msw' : "https://magicseaweed.com/La-Cote-Sauvage-Surf-Report/1556/"},
     'Etretat' :
        {'surf_report' : "https://www.surf-report.com/meteo-surf/etretat-s1022.html",
         'msw' : "http://fr.magicseaweed.com/Etretat-Surf-Report/80/"},
     'Siouville' :
        {'surf_report' : "https://www.surf-report.com/meteo-surf/siouville-s1079.html",
         'msw' : "http://fr.magicseaweed.com/Siouville-Surf-Report/1547/"},
     'Vendee' :
        {'surf_report' : "https://www.surf-report.com/meteo-surf/bud-bud-s1005.html",
         'msw' : "http://fr.magicseaweed.com/Les-Conches-Bud-Bud-Surf-Report/1573/"},
     'La_torche' :
        {'surf_report' : "https://www.surf-report.com/meteo-surf/la-torche-s1040.html",
         'msw' : "http://fr.magicseaweed.com/La-Torche-Surf-Report/72/"},
     'Seignosse' :
        {'surf_report' : "https://www.surf-report.com/meteo-surf/les-casernes-seignosse-s1187.html",
         'msw' : "http://fr.magicseaweed.com/Casernes-Surf-Report/1175/"}
    }
    spot = commande.split(' ')[1]
    site = 'msw'
    driver = webdriver.PhantomJS(os.getcwd()+"/bin/phantomjs")
    driver.set_window_size(840,620)
    #bot.send_text_message(recipient_id,'''Got you ! J'ouvre le site...''')
    driver.get(url[spot][site])
    #bot.send_text_message(recipient_id,'''Je choppe les prévisions...''')
    driver.save_screenshot(os.getcwd()+'/report_'+recipient_id+'.png')
    #bot.send_text_message(recipient_id,'''Je les mets en forme...''')
    img = Image.open(os.getcwd()+'/report_'+recipient_id+'.png')
    w, h = img.size
    img = img.crop((15,0,w,h-3755)).save(os.getcwd()+'/report_'+recipient_id+'.png')
    print('Image récupérée')
    #bot.send_text_message(recipient_id,'''Je les enregistre...''')
    return 'success'

def send_report(recipient_id):
    params = {
        "access_token": os.environ["ACCESS_TOKEN"]
    }
    data = {
        # encode nested json to avoid errors during multipart encoding process
        'recipient': json.dumps({
            'id': recipient_id
        }),
        # encode nested json to avoid errors during multipart encoding process
        'message': json.dumps({
            'attachment': {
                'type': 'image',
                'payload': {}
            }
        }),
        'filedata': (os.path.basename('report_'+recipient_id+'.png'), open('report_'+recipient_id+'.png', 'rb'), 'image/png')
    }

    # multipart encode the entire payload
    multipart_data = MultipartEncoder(data)

    # multipart header from multipart_data
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=multipart_header, data=multipart_data)

    print('Image envoyée !')

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

if __name__ == "__main__":
    app.run()
