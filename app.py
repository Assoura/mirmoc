#Python libraries that we need to import for our bot
import json
import requests
from PIL import Image
from selenium import webdriver
from flask import Flask, request
from pymessenger.bot import Bot
import os
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
                if recipient_id != '1547681661986967':
                    bot.send_text_message('1547681661986967',recipient_id+' à envoyé : '+message['message']['text'])
                if message['message'].get('text'):
                    if "Mirmoc" in message['message']['text']:
                        try:
                            commande = message['message']['text']
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
                            site = commande.split(' ')[2]

                            #bot.send_text_message(recipient_id,'Je ne peux faire que ça pour le moment : '+url[spot][site])
                            #attach_url = 'https://github.com/Assoura/mirmoc/blob/master/report.png?raw=true'
                            #bot.send_text_message(recipient_id,'''Mais l'idéee est de faire ça :''')
                            #send_attachment(recipient_id, attach_url)

                            print(os.getcwd())
                            print(os.listdir(os.getcwd()))
                            driver = webdriver.PhantomJS(os.getcwd()+"/bin/phantomjs")
                            driver.set_window_size(840,620)
                            print("##################  Ouvre site")
                            driver.get(url[spot][site])
                            print("##################  Site ouvert")
                            driver.save_screenshot("/app/test.png")
                            print("##################  Screenshot fait")
                            print(os.listdir(os.getcwd()))
                        except:
                            bot.send_text_message(recipient_id,'''Désolé, je n'ai pas compris. Je ne connais que les site 'msw' et 'surf_report' et les spots 'Seignosse', 'Siouville', 'La_torche', 'Vendee', 'Quiberon' et 'Etretat'. Je ne comprends que la syntaxe 'Mirmoc spot site' ''')
                    else:
                        print(os.getcwd())
                        bot.send_text_message(recipient_id,'''Désolé, je n'ai pas compris. Je ne connais que les site 'msw' et 'surf_report' et les spots 'Seignosse', 'Siouville', 'La_torche', 'Vendee', 'Quiberon' et 'Etretat'. Je ne comprends que la syntaxe 'Mirmoc spot site' ''')
                            #print("##################  Message reçu : "+message['message']['text'])
                            #get_message('Siouville')
                            #print("##################  Sortie fonction report")
                            #image_url = "/app/test.png"
                            #bot.send_text_message(recipient_id,'En maintenance... :(')
                        #try:
                            #bot.send_image_url(recipient_id, image_url)
                        #except:
                        #    print("##################  Erreur")
                        #else:
                        #    print("##################  Message envoyé")
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(spot):
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

    site = 'msw'
    print("##################  Start PhantomJS ")
    driver.set_window_size(840,620)
    print("##################  Ouvre site")
    driver.get(url[spot][site])
    print("##################  Site ouvert")
    driver.save_screenshot("/app/test.png")
    print("##################  Screenshot fait")
    #img = Image.open("report.png")
    #w, h = img.size
    #img = img.crop((15,h-8335,w,h-3755)).save("report.png")
    return 'success'

def send_attachment(send_id, attach_url):
    params  = {"access_token": os.environ['ACCESS_TOKEN']}
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"recipient": {
                        "id": send_id
                        },
                        "message": {
                            "attachment": {
                                "type": "image",
                                "payload": {
                                    "url": attach_url, "is_reusable": True
                                }
                            }
                        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

if __name__ == "__main__":
    app.run()

#print("#####"+os.getcwd())
