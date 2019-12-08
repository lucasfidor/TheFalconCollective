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
from datetime import timedelta
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
                requested = str(update.message.text).lower()
                if requested == "create":
                    update.message.reply_text("Creating your account now....")

                    firstname = user_data['first_name']
                    try:
                        lastname = user_data['last_name']
                    except:
                        lastname = user_data['first_name']
                    email = str(telegram_id) + str(random.randint(1000000,9999999)) + "@mrsir.bot"

                    try:
                        us.register(firstname, lastname, email)
                        try:
                            try:
                                us.set_username(user_data['username'])
                            except:
                                update.message.reply_text("Please set a username in your Telegram settings")
                            try:
                                us.getToken()
                                us.getAccount()
                                us.store()
                                update.message.reply_text("Account successfully created and linked with your telegram account! Now you can Live More Bank Less with these commands:\n\n'Get balance'\n\n'Generate OTP'\n\n'Transfer <amount> to <username/OTP/mobile> for <notes>'\n\n'Request <amount> from <username/OTP/mobile> for <notes>'\n\n*Notes are optional for transfers")
                            except:
                                update.message.reply_text("Error Creating Account (ERR:84)")
                        except:
                            update.message.reply_text("Error Creating Account (ERR:86)")
                    except:
                        print("REGISTER FAILED")
                        update.message.reply_text("Error Creating Account (ERR:89)")
                else:
                    new_user(update)
        else:
            # EXISTING USER COMMAND
            us.set_username(user_data['username'])
            if update.message:  # your bot can receive updates without messages
                requested = str(update.message.text).lower()
                if requested == "help":
                    update.message.reply_text("Live More Bank Less with these commands:\n\n'Get balance'\n\n'Generate OTP'\n\n'Transfer <amount> to <username/OTP/mobile> for <notes>'\n\n'Request <amount> from <username/OTP/mobile> for <notes>'\n\n*Notes are optional for transfers")

                if requested == "loremipsum":
                    us.add_points(5)
                    update.message.reply_text("You have earned 5 rewards point!\n\nPoint Balance: {}".format(us.rewards_point))

                if requested == "get balance":
                    update.message.reply_text("Balance: {}\nAvailable Balance: {}\n\nRewards Point: {}\nPoint Expiry: {}".format(us.balance, us.avail_balance, us.rewards_point, str(datetime.date.today()+timedelta(days=365))))

                try:
                    requested.index("transfer")
                    try:
                        requested.index(" to ")
                        try:
                            requested.index(" for ")
                            try:
                                amount = requested.lower().split(" to ")[0].split("transfer ")[1].replace(" ","")
                                receiver = requested.lower().split(" to ")[1].split(" for ")[0].replace(" ", "")
                                notes = requested.lower().split(receiver)[1]
                                tt = us.transfer(receiver, amount, notes)
                                if tt == "NOT FOUND":
                                    update.message.reply_text("Recipient username not found")
                                elif tt == "FAILED":
                                    update.message.reply_text("Unable to perform transfer.")
                                else:
                                    bot.send_message(int(tt), "You have received ${} from {}{}".format(amount, us.username, notes))
                                    update.message.reply_text("Successfully transferred ${} to {} (Acc No. {}){}".format(amount, receiver, tt, notes))
                                    us.add_points(5)
                                    update.message.reply_text(
                                        "You have earned 5 rewards point!\n\nPoint Balance: {}".format(
                                            us.rewards_point))
                            except:
                                update.message.reply_text("Unable to perform transaction.")
                        except:
                            try:
                                amount = requested.lower().split(" to ")[0].split("transfer ")[1].replace(" ", "")
                                receiver = requested.lower().split(" to ")[1].replace(" ", "")
                                tt = us.transfer(receiver, amount)
                                if tt == "NOT FOUND":
                                    update.message.reply_text("Recipient username not found")
                                elif tt == "FAILED":
                                    update.message.reply_text("Unable to perform transfer.")
                                else:
                                    bot.send_message(int(tt), "You have received ${} from {}".format(amount, us.username))
                                    update.message.reply_text("Successfully transferred ${} to {} (Acc No. {})".format(amount, receiver, tt))
                                    us.add_points(5)
                                    update.message.reply_text(
                                        "You have earned 5 rewards point!\n\nPoint Balance: {}".format(
                                            us.rewards_point))
                            except:
                                update.message.reply_text("Unable to perform transaction.")
                    except:
                        try:
                            try:
                                requested.index(" for ")
                                receiver = requested.lower().split(" ")[1]
                                amount = requested.lower().split(" ")[2]
                                notes = requested.lower().split(amount)[1]
                                tt = us.transfer(receiver, amount, notes)
                                if tt == "NOT FOUND":
                                    update.message.reply_text("Recipient username not found")
                                elif tt == "FAILED":
                                    update.message.reply_text("Unable to perform transfer.")
                                else:
                                    update.message.reply_text(
                                        "Successfully transferred ${} to {} (Acc No. {}){}".format(amount,
                                                                                                                receiver,
                                                                                                                tt,
                                                                                                                notes))
                                    bot.send_message(int(tt),
                                                     "You have received ${} from {}{}".format(amount, us.username,
                                                                                              notes))
                                    us.add_points(5)
                                    update.message.reply_text(
                                        "You have earned 5 rewards point!\n\nPoint Balance: {}".format(
                                            us.rewards_point))
                            except:
                                #transfer lucasliao 1000 for subway for national
                                receiver = requested.lower().split(" ")[1]
                                amount = requested.lower().split(" ")[2]
                                tt = us.transfer(receiver, amount)
                                if tt == "NOT FOUND":
                                    update.message.reply_text("Recipient username not found")
                                elif tt == "FAILED":
                                    update.message.reply_text("Unable to perform transfer.")
                                else:
                                    update.message.reply_text(
                                        "Successfully transferred ${} to {} (Acc No. {})".format(amount, receiver, tt))
                                    bot.send_message(int(tt), "You have received ${} from {}".format(amount, us.username))
                                    us.add_points(5)
                                    update.message.reply_text(
                                        "You have earned 5 rewards point!\n\nPoint Balance: {}".format(
                                            us.rewards_point))
                        except:
                            update.message.reply_text("*Missing Recipient\n\nFollow this format:\n\n'Get balance'\n\n'Generate OTP'\n\n'Transfer <amount> to <username/OTP/mobile> for <notes>'\n\n'Request <amount> from <username/OTP/mobile> for <notes>'\n\n*Notes are optional for transfers")
                except:
                    pass

                try:
                    requested.index("request")
                    try:
                        requested.index("from")
                        try:
                            requested.index("for")
                            try:
                                amount = requested.lower().split(" from ")[0].split("request ")[1].replace(" ", "")
                                requestee = requested.lower().split(" from ")[1].split(" for ")[0].replace(" ", "")
                                notes = requested.lower().split(requestee)[1]
                                telid = us.username_to_telegram_id(requestee)
                                if telid is not None:
                                    bot.send_message(telid, "{} is requesting ${}{}".format(us.username, amount, notes))
                                    update.message.reply_text("Requested!")
                                else:
                                    update.message.reply_text("Username not valid")
                            except:
                                update.message.reply_text("Unable to perform request.")
                        except:
                            update.message.reply_text("Please provide a request note.")
                    except:
                        update.message.reply_text("Please provide a username to request from.")
                except:
                    pass


            us.store()



def new_user(update):
    update.message.reply_text("You seem new! You need to create a banking account or link your existing account with us. Reply 'create' to create one now. Remember to set a username, it will come in handy!)")
    return


if __name__ == '__main__':
    main()


# RECOMMEND PLACES TO GO FOR DINNER BASE ON LOCATION AND BANK PROMO
# CHECK SPENDING CAPABILITY