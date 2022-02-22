import http

import telegram
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler,Filters
from telegram import ReplyKeyboardMarkup,Bot, ChatMember
import requests,json
import os
import redis
from datetime import date

r = redis.StrictRedis(host='localhost', port=6379, db=1)

config = json.load(open('config.json','r'))

TOKEN = config['token']
DEV = True

admins = config['admins']
data = []
dash_key = [['Twitter','Telegram','STB address'],['Balance','Email']]
admin_key = [['Users','Get List']]
stabila_group = config['stabilagroup']
contract_address = config['contract_address']
token_name = config['token name']
token_price = float(config['token price'])
token_qty = int(config['token qty'])

webhook_url = 'Your Webook'
PORT = int(os.environ.get('PORT','8443'))


def start(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        print(user)
        today = date.today()
        print("Today's date:", today)
        print(r.hget(user, 'TG'))
        if r.hget(user, 'TG')==None:
            r.hset(user, 'TG', user)
            print('New user registered')
            r.hset(user, 'created', str(today))
            r.hset(user, 'twitter', "")
            r.hset(user, 'stbaddress', "")
            r.hset(user, 'StabilaSTBjoined', "")
            r.hset(user, 'Ref1', "")
            r.hset(user, 'Ref2', "")
            r.hset(user, 'Ref3', "")
            r.hset(user, 'Ref4', "")
            r.hset(user, 'Ref5', "")
            r.hset(user, 'Ref6', "")
            r.hset(user, 'Ref7', "")
            r.hset(user, 'Balance', "")
            r.hset(user, "email","")
            #msg = 'Hi '+user+'. '+config['intro']
            #started_msg = 'TWITTER MESSAGE'
            #update.message.reply_text(msg)
            #update.message.reply_text(started_msg)
        print('este')
        value=token_price*token_qty
        print(value)
        welcome_msg = 'Hi '+ user + '\n'+config['intro']+' 🔥\n\nToken: '+token_name+' 💎\nQty: '+str(token_qty)+' 💰\nPrice: $'+str(token_price)+' 💲\nValue: $'+str(value)+' 💵\n\n📢\nPlease Proceed with Your Airdrop Registration⬇️'+'\n\n🔔To update twitter 🐦 type ⌨️:\ntwitter:username\n\n🔔To update stb address 👛 type ⌨️:\nstb address:address\n\n🔔To update email 📧 type ⌨️:\nemail:email address\n'
        print(welcome_msg)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(welcome_msg,reply_markup=reply_markup)

    else:
        msg = '{}. \nI don\'t reply in group, come in private'.format(config['intro'])
        update.message.reply_text(msg)

def twitter(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        twtr_user = r.hget(user, 'twitter').decode('UTF-8')
        msg = 'Your twitter username is:\n@{}'.format(twtr_user)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)


def get_twitterinfo(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        twitter_username = update.message.text
        twitter_username = str.lower(twitter_username)
        # TODO: do what you want with book name

        answer = f'Your twitter  have wrote me {twitter_username}'
        twitter_username = twitter_username.split(':')
        update.message.reply_text(twitter_username[1])
        r.hset(user, 'twitter', twitter_username[1])

def get_email(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        email_username = update.message.text
        email_username = str.lower(email_username)
        # TODO: do what you want with book name

        answer = f'Your email is {email_username}'
        email_username = email_username.split(':')
        update.message.reply_text(email_username[1])
        r.hset(user, 'email', email_username[1])

def get_stbaddress(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        stb_address = update.message.text
        stb_address = stb_address.split(':')
        update.message.reply_text(stb_address[1])
        r.hset(user, 'stbaddress', stb_address[1])

def telegramin(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        telegram_user = r.hget(user, 'StabilaSTBjoined').decode('UTF-8')
        msg = 'Join Stabila Telegram Group at '+stabila_group+' {}'.format(telegram_user)+'\nStatus:'+r.hget(user, 'StabilaSTBjoined').decode('UTF-8')

        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)


def stb(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        stb_addr = r.hget(user, 'stbaddress').decode('UTF-8')
        msg = 'Please register at https://stabilascan.org to create your wallet.\n\nYour stb address is:\n{}'.format(stb_addr)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)


def link(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        msg = 'https://t.me/{}?start={}'.format(config['botname'],data['id'][user])
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)


def extra(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if data["process"][user] == 'twitter':
            data['twitter'][user] = update.message.text
            data['process'][user] = 'discord'
            json.dump(data,open('users.json','w'))
            update.message.reply_text("DISCORD MESSAGE")
        elif data["process"][user] == 'discord':
            data['discord'][user] = update.message.text
            data['process'][user] = "stb"
            json.dump(data,open('users.json','w'))
            update.message.reply_text("WALLET MESSAGE")
        elif data["process"][user] == 'stb':
            data['stb'][user] = update.message.text
            data['process'][user] = "finished"
            json.dump(data,open('users.json','w'))
            msg = "DASHBOARD MESSAGE!"
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)
        else:
            msg = "Please select one of the options."
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)


def admin(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user in admins:
            msg = "Welcome to Admin Dashboard"
            reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)

def users(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user in admins:
            msg = "A total of {} have joined this program".format(data['total']-1000)
            reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)


def bal(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        stb_address = r.hget(user,'stbaddress').decode('UTF-8')
        print(contract_address)
        print(stb_address)
        conn = http.client.HTTPSConnection("apilist.stabilascan.org")

        payload = '''{"addresses": ["'''+contract_address+'''"]}'''
        print(payload)
        #payload = json.dumps(payload)
        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/src20_balance/"+stb_address, payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        print(type(data))
        bal = float((data['data'][0]['balance'])/1000000)
        print(bal)


        r.hset(user, 'Balance', bal)
        msg = "You have {} tokens".format(bal)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)

def email(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        email = r.hget(user, 'email').decode('UTF-8')
        msg = 'Your email address is:\n{}'.format(email)
        reply_markup = ReplyKeyboardMarkup(dash_key, resize_keyboard=True)
        update.message.reply_text(msg, reply_markup=reply_markup)

if __name__ == '__main__':
    data = json.load(open('users.json','r'))
    updater = Updater(TOKEN,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.regex("start"),start))
    dp.add_handler(CommandHandler("admin",admin))
    dp.add_handler(MessageHandler(Filters.regex("^Twitter$"),twitter))
    dp.add_handler(MessageHandler(Filters.regex("^Telegram$"), telegramin))
    dp.add_handler(MessageHandler(Filters.regex("^STB address$"),stb))
    dp.add_handler(MessageHandler(Filters.regex("^Users$"),users))
    dp.add_handler(MessageHandler(Filters.regex("^Balance$"),bal))
    dp.add_handler(MessageHandler(Filters.regex("^Email$"),email))
    dp.add_handler(MessageHandler(Filters.regex("^twitter:"), get_twitterinfo))
    dp.add_handler(MessageHandler(Filters.regex("^email:"), get_email))
    dp.add_handler(MessageHandler(Filters.regex("^stb address:"), get_stbaddress))
    dp.add_handler(MessageHandler(Filters.text,extra))
    if DEV is not True:
        updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
        updater.bot.set_webhook(webhook_url + TOKEN)
    else:
        updater.start_polling()
    print("Bot Started")
    updater.idle()
