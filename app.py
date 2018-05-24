#Python libraries that we need to import for our bot
import random
from PIL import Image
from selenium import webdriver
from flask import Flask, request
from pymessenger.bot import Bot
import os
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
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
                if message['message'].get('text'):
                    if "Mirmoc" in message['message']['text']:
                        try:
                            get_message(message['message']['text'])
                        except:
                            bot.send_text_message(recipient_id, 'You fuck my wife ?!')
                        else:
                            bot.send_image(recipient_id, "report.png")
                else:
                    bot.send_text_message(recipient_id, 'Not for me but got it!')
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

	driver = webdriver.PhantomJS()
	driver.set_window_size(840,620)
	driver.get(url[spot][site])
	driver.save_screenshot('report.png')
	img = Image.open("report.png")
	w, h = img.size
	img = img.crop((15,h-8335,w,h-3755)).save("report.png")
    return 'success'

if __name__ == "__main__":
    app.run()
