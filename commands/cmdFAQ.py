def get_faq(bot, update, args):
	import yaml
	faq_file = './faq.yml'
	score_dict = {'':''}
	with open(faq_file, 'r') as ymlfile:
		cfg = yaml.load(ymlfile)
		for id in cfg:
			for item in args:
				wordcount = 0
				if item in cfg[id]['words']:
					wordcount += 1
					score_dict[cfg[id]['id']] = 
			answer=cfg[id]['answer']
			bot.sendMessage(update.message.chat_id, text=answer)
