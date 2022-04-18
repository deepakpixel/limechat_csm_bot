# import required modules
from cgitb import text
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from telegram import ParseMode


import base64

user_chat={}
# DEEPAK
# updater.bot.send_message(chat_id="1086309772", text=update.message.text)
# Gautami
# updater.bot.send_message(chat_id="1363282180", text=update.message.text)
# Atharva
# updater.bot.send_message(chat_id="1396626290", text=update.message.text)

user_chat["deepakjangra"]=1086309772
user_chat["panda_1697"]=1363282180
user_chat["atharva"]=1086309772

loggedin=False
BOT_TOKEN="5180983586:AAEEKqXJbSCValnp4v3yKL8nRlGaQPOmtdo"


def teleSend(user, content):
    global user_chat
    print("\nTELESENDING",content, user)
    try:
      # updater.bot.send_message(chat_id=user_chat[user], text=content)
      updater.bot.send_message(chat_id=user_chat[user], text=content, parse_mode='MarkdownV2')

    except Exception as e:
      print("ERROR WHILE TELESENDING", e)

def anyMessage(update, context):
    global user_chat
    user_chat[update.message.from_user.username] = update.message.chat.id
    try:
      # print(update.message)
      print("\n")
      print("CHATID", update.message.chat.id)
      print("MESSAGE: ", update.message.text)
      print("USER: ", update.message.from_user.first_name)
      print("USERNAME", update.message.from_user.username)
      msg=update.message.text
      username=update.message.from_user.username

      if(not update.message):
        return
      if(msg.lower().strip() in ['hi','hey','hello','hey there']):
        s='''
Hi, I am LimeChat CSM bot\.
How can I help you today?
If you have any query please drop here in the format "DOUBT: Here comes the doubt"
'''
        teleSend(update.message.from_user.username, s)
        return

      if(msg.lower().strip() in ['any update?', "status?", "update", "?", "any update on this?"]):
        s='''
Our CSM Team is looking into your ticket\. It is expected to be resolved by tomorrow\. I will remind the concerned CSM in case you don't get any resolution by tomorrow\.
'''
        teleSend(update.message.from_user.username, s)
        return

      # make call
      url = 'http://localhost:3333/create-ticket'
      myobj = {'contact_id': update.message.from_user.username,
                'title': update.message.text
              }

      x = requests.post(url, data = myobj)
      print(x.json())
      print("ready")
      try:
        for i in x.json()['sendMessages']:
          teleSend(
            i["username"],
            i["content"]
          )
      except:
        pass


      # if("username" in x.text):
      #   teleSend(x.text.username.)

      # DEEPAK
      # updater.bot.send_message(chat_id="1086309772", text=update.message.text)
      # Gautami
      # updater.bot.send_message(chat_id="1363282180", text=update.message.text)
      # Atharva
      # updater.bot.send_message(chat_id="1396626290", text=update.message.text)
      # teleSend("No google meet link found in the message")
    except:
      pass

def help(update, context):
    s='''
Hi, I am LimeChat CSM bot\.
How can I help you today?
If you have any query please drop here in the format\.
"*BUG: Here comes the bug*"
or
"*REQUEST: Here comes the request*"
or
"*DOUBT: Here comes the doubt*"

We support *BUG*, *REQUEST*, *DOUBT* as of now\. 
'''
#     s='''
# Hi, I am LimeChat CSM bot\.
# How can I help you today?
# If you have any query please drop here in the format "DOUBT: Here comes the doubt"
# '''
    teleSend(update.message.from_user.username, s)

def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)
    # teleSend(context.error)

updater = Updater(BOT_TOKEN, use_context=True)

dp = updater.dispatcher
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("start", help))
dp.add_handler(MessageHandler(Filters.all,anyMessage))

dp.add_error_handler(error)


# Start the Bot
updater.start_polling()

updater.idle()

print("BOT running")