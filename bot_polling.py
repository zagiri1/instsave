import json
import requests
from requests import get,post
from sistem import Bot
from config import *

api = f"https://api.telegram.org/bot{token_bot}/"
update_id = 0

print("Бот запущен")
print("Нажми CTRL + C чтобы оффнуть бота")
while True:
	try:
		req = get(f"https://api.telegram.org/bot{token_bot}/getupdates",params={"offset":update_id}).json()
		if len(req['result']) == 0:
			continue
		try:
			update = req["result"][0]
			Bot(update)
			update_id = update['update_id'] + 1
			print("-"*40)
		except KeyError:
			continue
	except KeyboardInterrupt:
		exit()
	except requests.exceptions.ConnectionError:
		continue