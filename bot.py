import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import os
import json

BOT_TOKEN = "BOT TOKEN HERE"


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi!')


def help(update, context):
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Help!')


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def file_handler (update, context):
	chatid = str(update.message.chat.id)
	if not chatid in chatidfolder:
		folder = input(f"New chat (id={chatid})\n> Enter folder: ")
		chatidfolder[chatid] = folder
		with open("chatidfolder.json", "w") as jsonFile:
			json.dump(chatidfolder, jsonFile)
	else:
		folder = chatidfolder[chatid]
	try:
		os.chdir(folder)
	except:
		os.mkdir(folder)
		os.chdir(folder)
	fileID = update.message['document']['file_id']
	file = context.bot.getFile(fileID)
	file.download(update.message['document']['file_name'])
	os.chdir("../")

def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(BOT_TOKEN, use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))

	dp.add_handler(MessageHandler(Filters.document, file_handler))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	with open("chatidfolder.json", "r") as jsonFile:
		chatidfolder = json.load(jsonFile)
	main()