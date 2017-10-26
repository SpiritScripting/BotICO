#!/usr/bin/python3

from uuid import uuid4
import re
import telegram
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters
import logging
import argparse
# Command modules
import commands.cmdFAQ

method = ''
token = ''

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)



def help(bot, update):
	help_message = 'Use\n\
			More info: '
	bot.sendMessage(update.message.chat_id, text=help_message)

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def unknown(bot, update):
	bot.sendMessage(update.message.chat_id, text="Unknown command... (/help)")

def main():
	import yaml

	cfg_file = './config/botcfg.yml'
	with open(cfg_file, 'r') as ymlfile:
		cfg = yaml.load(ymlfile)
	token = cfg['token']
	bot = telegram.Bot(token=token)


	updater = Updater(token)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("question", cmdFAQ.get_faq, pass_args=True))
	updates = bot.getUpdates()
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()

