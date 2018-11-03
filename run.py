'''from flask import Flask
app = Flask(__name__)

@app.route("/sms")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)
'''
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client 

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    account_sid = 'AC19b42bbad5c3281b12200c3ceed78c1a' 
    auth_token = 'b71438e2d6a16e9a6a3e173a5a5265f2' 
    client = Client(account_sid, auth_token) 
    url = 'https://github.com/Assoura/mirmoc/blob/master/temp.png?raw=true'
    num = client.messages.list()[0].from_
    client.messages.create(from_='whatsapp:+14155238886',  
                           body='With love :)',      
                           to='whatsapp:'+num, 
                           media_url=url) 
    
    client.messages.create(from_='+33644640350',  
                           body="Prévisions envoyées a :"+num,      
                           to='+33682444721') 
    return str(1)


if __name__ == "__main__":
    app.run(debug=True)
#https://demo.twilio.com/welcome/sms/reply/    