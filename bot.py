from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

global count
count = 4
updater = Updater(token=config.Token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi, I am a data collection bot for ValteRego. Please key in your training statement.")
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

emotions={1:{1:"serenity",2:"joy",3:"ecstasy"},
            2:{1:"pensiveness",2:"sadness",3:"grief"},
            3:{1:"acceptance",2:"trust",3:"admiration"},
            4:{1:"boredom",2:"disgust",3:"loathing"},
            5:{1:"apprehension",2:"fear",3:"terror"},
            6:{1:"annoyance",2:"anger",3:"rage"},
            7:{1:"distraction",2:"surprise",3:"amazement"},
            8:{1:"interest",2:"anticipation",3:"vigilance"}}

def list(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=str(emotions))
    
list_handler = CommandHandler('list', list)
dispatcher.add_handler(list_handler)


responsetext1 = """Thank you for your input. Among the 8 emotions below, which response would you expect? Please key in a number. Alternatively, you may use /list command to find out the full list of emotions.
1. Joy
2. Sadness
3. Trust
4. Disgust
5. Fear
6. Anger
7. Surprise
8. Anticipation
"""

global response1
response1 = 1

responsetext3 = """Thank you for your input!""" 

def trigger(update, context):
    global count
    global response1
    if (count%3==1):
        context.bot.send_message(chat_id=update.message.chat_id, text=responsetext1)
        sheet.update_cell((count//3)+1, 1, update.message.text)
    elif (count%3==2):
        response1 = int(update.message.text)
        
        responsetext2 = ("""From a scale of 1-3, 3 being the most severe, how would you rate the intensity of the emotion?
1. %s
2. %s
3. %s
""" % (emotions[response1][1],emotions[response1][2],emotions[response1][3]))
        
        context.bot.send_message(chat_id=update.message.chat_id, text=responsetext2)
        sheet.update_cell((count//3)+1, 2, update.message.text)
    else:
        response2 = int(update.message.text)
        context.bot.send_message(chat_id=update.message.chat_id, text=responsetext3)
        sheet.update_cell((count//3), 3, update.message.text)
        sheet.update_cell((count//3), 4, emotions[response1][response2])
    count+=1

trigger_handler = MessageHandler(Filters.all,trigger)
dispatcher.add_handler(trigger_handler)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Telebot Data").sheet1


updater.start_polling()