import logging
import time

import telegram
import json
import user
import ast
from telegram.error import NetworkError, Unauthorized
from time import sleep
from processor import config
import datetime
from processor.Sandbox_Api import SandboxApi
import random
global user_data


def main():

    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('1016014446:AAFMZl0DY3setFLi8u4OcfIvbi99MEon7iU')

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
        print(update)
        us = user.User(update.message.from_user.id)
        value = str(update.message.from_user).replace("\'", "\"")
        user_data = ast.literal_eval(value)
        telegram_id = update.message.from_user.id

        if(us.load() is False):
            # NON EXISTING USER COMMAND
            if update.message:  # your bot can receive updates without messages
                requested = str(update.message.text)
                if requested == "Create":
                    update.message.reply_text("Creating your account now....")

                    firstname = user_data['first_name']
                    try:
                        lastname = user_data['last_name']
                    except:
                        lastname = user_data['first_name']
                    email = str(telegram_id) + "@mrsir.bot"

                    try:
                        us.register(firstname, lastname, email)
                        us.set_username(user_data['username'])
                        us.getToken()
                        us.getAccount()
                        us.store()
                        update.message.reply_text("Account successfully created and linked with your telegram account! Now you can simply bank with these commands:\n\n'Get balance'\n'Generate OTP'\n'Transfer <amount> to <username/OTP/mobile> with <notes>'")
                    except:
                        print("REGISTER FAILED")
                        update.message.reply_text("Error Creating Account")
                else:
                    new_user(update)
        else:
            # EXISTING USER COMMAND
            us.set_username(user_data['username'])
            if update.message:  # your bot can receive updates without messages
                requested = str(update.message.text).lower()
                if requested == "help":
                    update.message.reply_text("simply bank with these commands:\n\n'Get balance'\n'Generate OTP'\n'Transfer <amount> to <username/OTP/mobile>'\n'Transfer <amount> to <username/OTP/mobile> for <notes>'")

                if requested == "get balance":
                    update.message.reply_text("Balance: {}\nAvailable Balance: {}".format(us.balance, us.avail_balance))

                try:
                    requested.index("transfer")
                    try:
                        requested.index("to")
                        try:
                            requested.index("for")
                            try:
                                amount = requested.lower().split("to")[0].split("transfer")[1].replace(" ","")
                                receiver = requested.lower().split("to")[1].split("for")[0].replace(" ", "")
                                notes = requested.lower().split("for")[1].replace(" ", "")
                                tt = us.transfer(receiver, amount, notes)
                                if tt == "NOT FOUND":
                                    update.message.reply_text("Recipient username not found")
                                elif tt == "FAILED":
                                    update.message.reply_text("Unable to perform transfer.")
                                else:
                                    update.message.reply_text("Successfully transferred ${} to {} (Acc No. {}) with notes: {}".format(amount, receiver, tt, notes))
                                    bot.send_message(913918081, "You have received ${} from {}".format(amount, us.username))
                            except:
                                update.message.reply_text("Unable to perform transaction.")
                        except:
                            try:
                                amount = requested.lower().split("to")[0].split("transfer")[1].replace(" ", "")
                                receiver = requested.lower().split("to")[1].replace(" ", "")
                                tt = us.transfer(receiver, amount)
                                if tt == "NOT FOUND":
                                    update.message.reply_text("Recipient username not found")
                                elif tt == "FAILED":
                                    update.message.reply_text("Unable to perform transfer.")
                                else:
                                    update.message.reply_text("Successfully transferred ${} to {} (Acc No. {})".format(amount, receiver, tt))
                                    bot.send_message(913918081, "You have received ${} from {}".format(amount, us.username))
                            except:
                                update.message.reply_text("Unable to perform transaction.")
                    except:
                        update.message.reply_text("*Missing Recipient*.\nFollow this format:\n'Transfer <amount> to <username/OTP>'\n^ without notes\n\n'Transfer <amount> to <username/OTP> for <notes>'\n^ with notes")
                except:
                    pass
            us.store()



def new_user(update):
    update.message.reply_text("You seem new! You need to create a banking account or link your existing account with us. Reply 'create' to create one now.)")
    return


if __name__ == '__main__':
    main()


# RECOMMEND PLACES TO GO FOR DINNER BASE ON LOCATION AND BANK PROMO
# CHECK SPENDING CAPABILITY