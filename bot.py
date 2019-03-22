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

responsetext2 = """From a scale of 1-3, 3 being the most severe, how would you rate the intensity of the emotion?"""

responsetext3 = """Thank you for your input!""" 

def trigger(update, context):
    global count
    if (count%3==1):
        context.bot.send_message(chat_id=update.message.chat_id, text=responsetext1)
        sheet.update_cell((count//3)+1, 1, update.message.text)
    elif (count%3==2):
        context.bot.send_message(chat_id=update.message.chat_id, text=responsetext2)
        sheet.update_cell((count//3)+1, 2, update.message.text)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=responsetext3)
        sheet.update_cell((count//3), 3, update.message.text)
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