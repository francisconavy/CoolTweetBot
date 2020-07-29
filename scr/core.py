from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from conf.settings import TELEGRAM_TOKEN, password

import twitter
import csv

def get_allowlist():
    allowlist = list()
    with open('conf/allowlist.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            allowlist.append(row[0])
    return allowlist

def start(update, context):
    response_message = "Have a cool idea? Tweet it!"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_message
    )

def auth(update, context):
    if context.args[0] == password:
        with open('conf/allowlist.csv', 'a+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([update.message.from_user['username']])
        response_message = "You're in the allowlist"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message
        )
    else:
        response_message = "Wrong Password"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message
        )


def tweetit(update, context):
    allowlist = get_allowlist()
    if update.message.from_user['username'] in allowlist:
        response_message = "Tweeting: "+update.message.text
        twitter.tweet(update.message.text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message
        )
    else:
        response_message = "You are not in the allowlist"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_message
        )



def unknown(update, context):
    response_message = "Unknown command"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_message
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('auth', auth)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), tweetit)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()