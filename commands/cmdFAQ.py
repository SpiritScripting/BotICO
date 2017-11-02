def get_faq(bot, update, args):
	import yaml
	faq_file = 'config/faq.yml'
	score_dict = {'':''}
	with open(faq_file, 'r') as ymlfile:
		cfg = yaml.load(ymlfile)
		for id in cfg:
			wordcount = 0
			for item in args:
				if item in cfg[id]['words']:
					wordcount += 1
			score_dict[cfg[id]['id']] = wordcount
		max = 0
		key_max = 0
		for key, value in score_dict.items():
			if value != '':
				if int(value) > max:
					max = int(value)
					key_max = int(key)
		if key_max != 0:
			answer=cfg[key_max]['answer']
		else:
			answer='I dont know, sorry.'
	bot.sendMessage(update.message.chat_id, text=answer)
