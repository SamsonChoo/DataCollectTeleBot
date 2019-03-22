from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

global count
count = 1
updater = Updater(token=config.Token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi, I am a data collection bot for ValteRego. Please key in your training statement.")
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def trigger(update, context):
    global count
    context.bot.send_message(chat_id=update.message.chat_id, text="哈咯小鱼尾")
    sheet.update_cell(count, 1, update.message.text)
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