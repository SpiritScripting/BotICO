def get_ico(bot, update, args):
	import requests
	import json
	answer = requests.get('https://etherchain.org/api/blocks/count').json()['data'][0]['count']
	bot.sendMessage(update.message.chat_id, text=answer)
