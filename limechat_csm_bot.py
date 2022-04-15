# import required modules 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
import time 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.update import Update
# from pymongo import MongoClient
# from pprint import pprint
import base64
# import requests


BOT_TOKEN="5180983586:AAEEKqXJbSCValnp4v3yKL8nRlGaQPOmtdo"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi, please reply to this message with your concern. Start your message with the word ‘Bug:’ , ‘Doubt:’ or ‘Request:’ depending on the nature of your message. ")


################################################
#               TELEGRAM BOT                   #
################################################


def teleSend(content, photo=False):
    try:
      if(content):
        updater.bot.send_message(content)
      if(photo):
        photo = base64.b64decode(photo)
        updater.bot.send_photo(photo)
    except:
      print("No content found")

def anyMessage(update, context):
    try:
      if(not update.message):
        return
      s=update.message.text.split(':',1).strip()
      # type=['Bug','Doubt','Request']
      for i in range(0, len(s)):
        if ('Bug' or 'Request' or 'Doubt') in s[i]:
          teleSend("Thanks for sharing your issue. The concerned person has been notified about the issue and will soon contact you.")
    except:
      teleSend('Error while joining',driver.get_screenshot_as_base64())


# def createticket(user_id, content):
#   try:
#     if()

def help(update, context):
    s='''COMMANDS 
/status 
/smart 
/leave 
/help 
/login 
/join (*deprecated)'''
    teleSend(s)

updater = Updater(BOT_TOKEN, use_context=True)

dp = updater.dispatcher
dp.add_handler(CommandHandler("Hi", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("commands", help))
dp.add_handler(MessageHandler(Filters.all,start))
dp.add_handler(MessageHandler(Filters.text,anyMessage)
# dp.add_error_handler(error)


# Start the Bot
updater.start_polling()

updater.idle()