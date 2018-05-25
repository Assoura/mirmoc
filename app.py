#Python libraries that we need to import for our bot
import json
import requests
from PIL import Image
from selenium import webdriver
from flask import Flask, request
from requests_toolbelt import MultipartEncoder
from pymessenger.bot import Bot
import os

driver = webdriver.PhantomJS(os.getcwd()+"/bin/phantomjs")
driver.set_window_size(840,620)

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN'] #EAAZAm0NGhNvoBABPn6MhEJGxN2Hhw37GZC53iXBOUDqGEbHsPV03ZCZCHSWnaW5y4q8a1H2gb5SC8VNKQKnfvMV0ucD03cPaeDnnovXzibahv6SapNJOWQd10UvG1sO0TtW4qE3kFx652tzLeA1tOh12xoZBZA4qo6uPsXTTIZCfAZDZD
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                commande = message['message']['text']
                print(recipient_id+' a envoyé : '+commande)
                if message['message'].get('text') and "Mirmoc" in message['message']['text']:
                    try:
                        print('try...')
                        scraping(commande,recipient_id)
                        send_report(recipient_id)
                    except:
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
    try:
        site = 'msw'
        url = {'Quiberon' :
            {'surf_report' : "https://www.surf-report.com/meteo-surf/sainte-barbe-s1169.html",
             'msw' : "http://fr.magicseaweed.com/La-Cote-Sauvage-Surf-Report/1556"},
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
        #bot.send_text_message(recipient_id,'''Got you ! Je cherche...''')
        driver.get(url[spot][site])
        #bot.send_text_message(recipient_id,'''Trouvé ! Je choppe les prévisions...''')
        print(os.listdir(os.getcwd()))
        driver.save_screenshot(os.getcwd()+'/report.png')
        #bot.send_text_message(recipient_id,'''Je les mets en forme...''')
        img = Image.open(os.getcwd()+'/report.png')
        w, h = img.size
        print(h)
        print(w)
        img = img.crop((15,0,w,h-3755)).save(os.getcwd()+'/report.png')
        print(os.listdir(os.getcwd()))
        #bot.send_text_message(recipient_id,'''Et voilà :''')
    except:
        bot.send_text_message(recipient_id,'''Je n'ai pas trouvé... Essayez avec un autre spot par exemple 'Mirmoc Siouville'. ''')
        print('Erreur scraping')

def send_report(recipient_id):
    try:
        params = {
            "access_token": os.environ["ACCESS_TOKEN"]
        }
        print(os.listdir(os.getcwd()))
        data = {
            # encode nested json to avoid errors during multipart encoding process
            'recipient': json.dumps({
                'id': recipient_id
            }),
            # encode nested json to avoid errors during multipart encoding process report_'+recipient_id+'
            'message': json.dumps({
                'attachment': {
                    'type': 'image',
                    'payload': {}
                }
            }),
            'filedata': (os.path.basename('report.png'), open('report.png', 'rb'), 'image/png')
        }

        # multipart encode the entire payload
        multipart_data = MultipartEncoder(data)

        # multipart header from multipart_data
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        print(os.listdir(os.getcwd()))
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=multipart_header, data=multipart_data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
    except:
        print('Erreur send_report')

if __name__ == "__main__":
    app.run()
