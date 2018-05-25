#Python libraries that we need to import for our bot
import json
import time
import requests
from PIL import Image
from selenium import webdriver
from flask import Flask, request
from requests_toolbelt import MultipartEncoder
from pymessenger.bot import Bot
import os

print('1')
driver = webdriver.PhantomJS(os.getcwd()+"/bin/phantomjs")
driver.set_window_size(840,620)

print('2')
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN'] #EAAZAm0NGhNvoBABPn6MhEJGxN2Hhw37GZC53iXBOUDqGEbHsPV03ZCZCHSWnaW5y4q8a1H2gb5SC8VNKQKnfvMV0ucD03cPaeDnnovXzibahv6SapNJOWQd10UvG1sO0TtW4qE3kFx652tzLeA1tOh12xoZBZA4qo6uPsXTTIZCfAZDZD
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

print('3')
#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
   print('8')
   output = request.get_json()
   print('9')
   for event in output['entry']:
      print('10')
      messaging = event['messaging']
      for message in messaging:
        print('11')
        if message.get('message'):
            print('12')
            recipient_id = message['sender']['id']
            commande = message['message']['text']
            if message['message'].get('text') and "Mirmoc" in message['message']['text']:
                try:
                    print('13')
                    scraping(commande,recipient_id)
                    send_report(recipient_id)
                except:
                    print('14')
                    bot.send_text_message(recipient_id,'''Désolé, je n'ai pas compris. Je ne connais que les spots 'Seignosse', 'Siouville', 'La_torche', 'Vendee', 'Quiberon' et 'Etretat'. Je ne comprends que la syntaxe 'Mirmoc spot' ''')
            else:
                print('15')
                bot.send_text_message(recipient_id,'''Désolé, je n'ai pas compris. Je ne connais que les spots 'Seignosse', 'Siouville', 'La_torche', 'Vendee', 'Quiberon' et 'Etretat'. Je ne comprends que la syntaxe 'Mirmoc spot' ''')
return "Message Processed"

#chooses a random message to send to the user
def scraping(commande,recipient_id):
    try:
        print('131')
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
        driver.get(url[spot][site])
        print(os.listdir(os.getcwd()))
        driver.save_screenshot(os.getcwd()+'/report.png')
        #img = Image.open(os.getcwd()+'/report.png')
        #w, h = img.size
        #img = img.crop((15,0,w,h-3755)).save(os.getcwd()+'/report.png')
        print('132')
    except:
        print('133')
        bot.send_text_message(recipient_id,'''Je n'ai pas trouvé... Essayez avec un autre spot par exemple 'Mirmoc Siouville'. ''')
        print('Erreur scraping')

def send_report(recipient_id):
    try:
        print('134')
        params = {
            "access_token": os.environ["ACCESS_TOKEN"]
        }
        print('135')
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
        print('136')
        # multipart encode the entire payload
        multipart_data = MultipartEncoder(data)
        # multipart header from multipart_data
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        print('137')
        print(os.listdir(os.getcwd()))
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=multipart_header, data=multipart_data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
    except:
        print('Erreur send_report')
        print('138')
