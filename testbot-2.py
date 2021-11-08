import os
import random
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN'] 
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] 
bot = Bot(PAGE_ACCESS_TOKEN)

def process_message(text):
    formatted_message = text.lower()

    greetings = ["Hi!", "Oh hello there!", "Greetings!", "Hello iskolar!", "Good day!"]
    thanks_response = ["You're welcome, happy to help 😊", "No problem, anytime!", "Happy to serve 😄", "My pleasure. If you have anymore concerns, don't hesitate to ask the people on this page 🙂"]
    number_reply = ["Here is the link that will hopfully answer your complaint.", "I hope the link below will help answer your complaint.", "Below is the link that will hopefully answer the complaint you have requested."]
    about_bot = ["Oh me?", "I see that you want to know more of me.", "You're curious about me, aren't you?", "I'm kind of new here so I understand why you asked."]

    if formatted_message == "1" or formatted_message == "one" or formatted_message == "first" or formatted_message == "1st":
        response = f"{random.choice(number_reply)} If you see that your question is not on the list, please comment on the page for assistance.\n\n[insert google doc link here]"
    elif formatted_message == "2":
        response = f"{random.choice(number_reply)} If you see that your question is not on the list, please comment on the page for assistance.\n\n[insert google doc link here]"
    elif formatted_message == "3":
        response = f"{random.choice(about_bot)} I was made by a student to assist the volunteers of this page in answering most of the common school queries. Other than that, I don't do much so please don't expect me to be like Alexa, Google Assistant, or other really smart AIs. I mean, it may be possible but it would take a very long time."
    elif formatted_message == "thank you" or formatted_message == "thankyou" or formatted_message == "thanks" or formatted_message == "ty" or formatted_message == "thx" or formatted_message == "salamat" or formatted_message == "salamuch" or formatted_message == "matsala" or formatted_message == "arigato" or formatted_message == "arigathanks":
        response = f"{random.choice(thanks_response)}"
    else:
        response = f"{random.choice(greetings)} I'm ASH your Automated Student Helper, how may I help you today? Please type in the number of your choice:\n\n[1]Enter complaint topic here\n[2]Enter complaint topic here\n[3]Why were you made?\n\n(Note: I'm just a simple bot so I'll keep repeating this response when you enter in a random text even if I don't understand it.)"
    return response

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['POST', 'GET'])

def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")

        else:
            return 'Bot not connected to Facebook.'

    elif request.method == "POST":
        payload = request.json
        event = payload['entry'][0]['messaging']

        for msg in event:
            text = msg['message']['text']
            sender_id = msg['sender']['id']

            response = process_message(text)
            bot.send_text_message(sender_id, response)

        return "Message received"

    else:
        return "200"


if __name__ == "__main__":
    app.run()
#https://fb-testbot-1.herokuapp.com/