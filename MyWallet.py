import logging
import telegram
import json
from telegram.error import NetworkError, Unauthorized
from time import sleep
from processor import config
import datetime
from processor.Sandbox_Api import SandboxApi
import random
global user_data

update_id = None
balances = {"000000":999999}

def main():

    with open(config.cdat, 'r') as cdat:
        global user_data
        user_data = json.load(cdat)
    cdat.close()

    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('981647694:AAHiFrTgzYr_qGl5ez9E10cPhMW_hh_i9QA')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        with open(config.logf, 'a') as logFile:
            logFile.write(str(datetime.datetime.today())+" ----- " + str(update.message.from_user.id) +" ----- "+str(update.message.text)+"\n")
        logFile.close()

        tele_id = update.message.from_user.id
        user_info = ""
        try:
            user_info = user_data[str(tele_id)]
        except:
            user_info = None

        if user_info == None:
            new_user(update)
        else:
            action = get_action(update)
            if(action is not None):
                update.message.reply_text(action)


        #if update.message:  # your bot can receive updates without messages
            #update.message.reply_text(update.message.from_user.id)
            #print(update.message.text)
            #message = str(update.message.text).lower()

def new_user(update):
    update.message.reply_text("You seem new! You need to link your account with us! Call 058 580 9686 to link now!")
    return


def get_action(update):
    print("Get Action")
    message = update.message.text.lower()
    auth = user_data[str(update.message.from_user.id)]["auth"]

    if (message == "my account"):
        return get_account(auth)
    elif(message == "balance"):
        return auth
    else:
        # TRANSFER
        try:
            message.index("transfer")
            try:
                message.index("to")
            except:
                update.message.reply_text("Missing receipient or the 'to' command")
        except:
            return auth

def get_account(auth):
    api = SandboxApi()
    response = api.get_accounts(auth)
    json_response = json.loads(response)
    firstname = json_response["data"][0]["customers"][0]["first_name"]
    lastname = json_response["data"][0]["customers"][0]["last_name"]
    balance = json_response["data"][0]["balance"]
    currency = json_response["data"][0]["currency"]
    overdraft = json_response["data"][0]["overdraft"]
    data = {}
    data["first_name"] = firstname
    data["last_name"] = lastname
    data["balance"] = balance
    data["currency"] = currency
    data["overdraft"] = overdraft

    text = "First Name: {}\nLast Name: {}\n\nAccount Balance: {}{}\nOverdraft: {}".format(firstname, lastname, currency, str(balance),str(overdraft))
    return text

if __name__ == '__main__':
    main()


# RECOMMEND PLACES TO GO FOR DINNER BASE ON LOCATION AND BANK PROMO
# CHECK SPENDING CAPABILITY