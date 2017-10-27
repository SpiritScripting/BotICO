def get_ico(bot, update, args):
	import json
	import requests
	import yaml
	dontknow = "Sorry. I don't know that information." 
	ethdiv = 1000000000000000000
	if len(args) <= 2:
		ico_file = 'config/ico.yml'
		with open(ico_file, 'r') as ymlfile:
			ico = yaml.load(ymlfile)
		conf_file = 'config/botcfg.yml'
		with open(conf_file, 'r') as ymlcfgfile:
			cfg = yaml.load(ymlcfgfile)	
		#### No arguments	
		if len(args) == 0:	
			answer = ico['info'];
		#### Commands with default second argument	
		elif len(args)==1:
			### ICO BLOCK
			if args[0] == 'block':
				answer = 'The current block in the Ethereum network is ' + str(requests.get('https://etherchain.org/api/blocks/count').json()['data'][0]['count'])
			### ICO START		
			elif args[0] == 'start':
				answer = (str(ico['name']) + ' Token Sale Starts in Block ' + str(ico['start'])) if str(ico['start']) != "" else dontknow
			### ICO COUNTDOWN
			elif args[0] == 'countdown':
				if ico['start'] == "":
					answer = dontknow
					blocksLeft = 0
				else:	
					blocksLeft = int(ico['start']) - requests.get('https://etherchain.org/api/blocks/count').json()['data'][0]['count']	
					blockTime = requests.get('https://etherchain.org/api/miningEstimator').json()['data'][0]['blockTime']
					timeLeft = blocksLeft * blockTime
					m, s = divmod(timeLeft, 60)
					h, m = divmod(m, 60)
					ftimeLeft = "%dh:%02dm:%02ds" % (h, m, s)
				if blocksLeft > 0:
					answer = ico['name'] + ' Token Sale Starts in ' + str(blocksLeft) + ' Blocks (' + str(ftimeLeft) + ').'
				elif blocksLeft < 0:
					answer = ico['name'] + ' Token Sale already started!'
			### ICO RAISED
			elif args[0] == 'raised':
				totalWithdrawls = 0
				internaltxList = requests.get('http://api.etherscan.io/api?module=account&action=txlistinternal&address=' + ico['contract'] + '&startblock=0&endblock=999999999&sort=asc&apikey=' + cfg['etherscan_token'] ).json()['result']
				ethprice = float(requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + cfg['etherscan_token']).json()['result']['ethusd'])
				for tx in internaltxList:
	 				totalWithdrawls = totalWithdrawls + int(tx['value'])/ethdiv			
				balance = int(requests.get('https://api.etherscan.io/api?module=account&action=balance&address=' + ico['contract'] + '&tag=latest&apikey=YourApiKeyToken' + cfg['etherscan_token'] ).json()['result'])/int(ethdiv)
				balanceUSD = "%.2f" % (float(balance) * ethprice)
				fbalance = "%.2f" % balance		
				totalRaised = "%.2f" % (totalWithdrawls + int(balance))
				raisedUSD = "%.2f" % (float(totalRaised) * ethprice)
				answer = ico['name'] + ' Has Raised : ' + str(totalRaised) + ' ether ($'+ str(raisedUSD) +') \nCurrent balance : ' + str(fbalance) + ' ether ($'+ str(balanceUSD) +')\n1 eth = $' + str(ethprice)
			elif args[0] == 'txs':
				txnum = 0	
				totalSent = 0
				txList = requests.get('http://api.etherscan.io/api?module=account&action=txlist&address=' + ico['contract'] + '&startblock=0&endblock=999999999&sort=asc&apikey=' + cfg['etherscan_token'] ).json()['result']
				for tx in txList:
					if tx['isError'] == '0':
						totalSent +=  int(tx['value'])/ethdiv	
						txnum+=1
				totalSent = "%.2f" % totalSent			
				answer = ico['name'] + " Token Sale has received\n" + str(txnum) + " valid transactions with "+ str(totalSent) + " ether so far.\nTotal txs : " + str(len(txList))		
			elif args[0] == 'contributors':
				txList = requests.get('http://api.etherscan.io/api?module=account&action=txlist&address=' + ico['contract'] + '&startblock=0&endblock=999999999&sort=asc&apikey=' + cfg['etherscan_token'] ).json()['result']
				cont_dict = {'':''}	
				for tx in txList:
					if tx['isError'] == '0':
						cont_dict[tx['from']]=int(tx['value'])/ethdiv
				answer = str(len(cont_dict)) + " different contributors have participated in the Token Sale."		
			elif args[0] == 'whales':
				txList = requests.get('http://api.etherscan.io/api?module=account&action=txlist&address=' + ico['contract'] + '&startblock=0&endblock=999999999&sort=asc&apikey=' + cfg['etherscan_token'] ).json()['result']
				cont_dict = {'': 0 }	
				whalecount = 0
				answer = 'These are the current whales of the Token Sale:\n'	
				for tx in txList:
					if tx['isError'] == '0':
						cont_dict[tx['from']] = int(tx['value'])/int(ethdiv)
				orderdict = [(k, cont_dict[k]) for k in sorted(cont_dict, key=cont_dict.get, reverse=True)]
				for k, v in orderdict:
					if whalecount<10:
						answer = answer + "%s: %.2f \n" % (k, v)
					whalecount += 1
		elif len(args)==2:
			if args[0] == 'address':
				totalBalance = requests.get('https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=' + ico['contract'] + '&address=' + args[1] + '&tag=latest&apikey='+ cfg['etherscan_token'] ).json()['result']
				answer =  args[1] + ' : ' + str(int(totalBalance)/ethdiv)	+ " DIVX."
		elif len(args)>2:
			answer='Too Many Arguments. /help for help' 

	bot.sendMessage(update.message.chat_id, text=answer)
